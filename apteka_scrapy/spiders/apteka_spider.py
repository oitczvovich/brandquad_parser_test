import scrapy
import time
import re

from apteka_scrapy.settings import PARSER_CITY_ID, CATEGORY_BY_PARSING
from apteka_scrapy.items import AptekaScrapyItem


class AptekaSpiderSpider(scrapy.Spider):
    name = "apteka_spider"
    allowed_domains = ["apteka-ot-sklada.ru"]
    start_urls = CATEGORY_BY_PARSING

    def start_requests(self):
        """Передача cookies с указанием ID города."""
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        """Парсер для сбора SKU со страницы категории."""
        cookies = {
            'city': PARSER_CITY_ID,
        }
        all_links_SKU = response.css("a.goods-card__link::attr(href)")
        for SKU_link in all_links_SKU:
            yield response.follow(
                SKU_link,
                cookies=cookies,
                callback=self.parser_SKU
            )

        next_page = response.css(
            "li.ui-pagination__item_next a::attr(href)"
        ).get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    def parser_SKU(self, response):
        """Парсер для сбора данных со страницы SKU."""
        city = "".join(
            response.css('span.ui-link__text::text').get()
        ).strip()

        request_url = response.url
        page_SKU = response.css("div.layout-default__page")
        title_fresh = page_SKU.css("h1 span[itemprop='name']::text").get()
        title = self.search_features_in_desc(title_fresh)
        rpc = self.get_RPC(request_url)
        header_description = page_SKU.css("div.page-header__description ul")
        brand = self.get_brand(title["title_out"])
        price_data = self.get_price(response)
        count, in_stock = self.get_in_stock(response)
        description = " ".join(
            response.css("div.custom-html.content-text ::text").getall()
        )
        main_image, set_images = self.get_assets(response)
        metadata = self.create_metadate(title, description)

        data = {
            "city": city,  # Добавил город для возможность проверки условий заданий.
            "timestamp": int(time.time()),
            "RPC": rpc,
            "url": response.url,
            "title": title['title_out'],
            "marketing_tags": self.get_clean_text(
                header_description.css("span.ui-tag::text").getall()
                ),
            "brand": brand,
            "section": page_SKU.xpath(
                "//span[@itemprop='name']/text()"
                ).getall()[:-2],
            "price_data": {
            #  На сайте не системы скидок в original попадала самая низкая цена.
            #    "current": None,
                "original": price_data,
            #     'sale_tag': None
            },
            "stock": {
                "in_stock": in_stock,  # {bool} Должно отражать наличие товара в аптеках.
                "count": count, # {int} Если есть показывает количество точек в которых есть SKU.
            },
            "assets": {
                "main_image": main_image,  # {str} Ссылка на основное изображение товара
                "set_images": set_images,  # {list of str} Список оставшихся изображений товара если есть.
                # Данной информации на сайте нет.
                # "view360": [],  # {list of str}
                # "video": []  # {list of str}
            },
            "metadata": metadata,
            "variants": 1  # У SKU нет вариантов выбора
        }
        yield AptekaScrapyItem(data)

    def search_features_in_desc(self, title_in: str) -> dict:
        """Функция для поиска в название особенностей.\n
        result_dict - возвращает словарь.\n
        {
        title_out - заголово.\n
        weight -> str | None - вес изделия если указан.\n
        count - поиск количества в упаковке.
        }
        """
        regex_list = {
            "weight": r"(\d+(?:,\d+)?)\s*(кг|г|мл|мг)",
            "count": r"N\s+(\d+)"
        }
        title_out = title_in
        result_dict = {"title_out": title_out}
        for feature, regex in regex_list.items():
            try:
                match = re.search(regex, title_out)
                if match:
                    title_out = f"{title_out}, {match.group(0)}"
                    result_dict["title_out"] = title_out
                    result_dict[feature] = match.group(0)
            except Exception as e:
                raise TypeError(f"An error occurred: {e}")

        return result_dict

    def get_RPC(self, url: str) -> int:
        """Функция для получения уникального номера SKU из ссылки."""
        last_part = url.split("_")[-1]
        digits = int("".join(filter(str.isdigit, last_part)))
        return digits

    def get_clean_text(self, HTML_string):
        """Функция удаляет лишние пробельные символы."""
        texts = []
        for item in HTML_string:
            item = item.strip()
            texts.append(item)
        return texts

    def get_brand(self, title):
        """Функция для извлечения названия брэнда из заголовка."""
        regex_brand = r"^([A-ZА-ЯЁ][A-ZА-ЯЁa-zа-я]*)( [а-я]* ([A-ZА-Я][a-zа-я]*)| ([A-ZА-Я][a-zа-я]*))?"
        match = re.search(regex_brand, title)
        if match:
            return match.group()

    def get_price(self, response):
        """Функия для получения цены если она указан в карточке."""
        price_element = response.css(
            "div.goods-offer-panel .ui-button__content span::text"
            ).get()
        if price_element is not None:
            return price_element[3:-2]
        return []

    def get_in_stock(self, response):
        """Функция возвращает количество аптек в которых есть SKU.\n
        булевое знаечения True если есть в наличии и False если SKU нет.
        """
        regex = r"\b(\d+)\b"
        string = response.css("div.goods-offer-panel  span::text").get()
        match = re.search(regex, string)
        if match:
            result = match.group(1)
            return result, True
        return 0, False

    def get_assets(self, response: str) -> str | None:
        """Функция возвращает main_image - ссылк на главную картинку.\n
        В случаи если есть еще изображения возвращает список ссылок
        на оставшиеся изображения.\n
        set_images - список ссылок.
        """
        images_list = response.css(
            "li.goods-gallery__preview-item img::attr(src)"
        ).getall()
        main_image = f"https://{self.allowed_domains[0]}{images_list[0]}"
        set_images = []
        if len(images_list) > 1:
            print("len(images_list)", len(images_list))
            for image in images_list[1:]:
                print("image", image)
                link_image = f"https://{self.allowed_domains[0]}{image}"
                set_images.append(link_image)
        return main_image, set_images

    def create_metadate(self, title, description) -> dict:
        """
        Функция подготавливает данные для словаря metadate.
        Если в title были вес или количество указывается
        в словаря отдельной позицией.
        """
        keys_metadata = {
            "weight": "Вес",
            "count": "Количество в упаковке",
        }
        metadata = {
            "__description": description,
        }
        for title_key, title_values in title.items():
            for meta_key, meta_name in keys_metadata.items():
                if title_key == meta_key:
                    metadata[meta_name] = title_values
        return metadata

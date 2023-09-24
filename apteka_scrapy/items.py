import scrapy


class AptekaScrapyItem(scrapy.Item):
    city = scrapy.Field()

    timestamp = scrapy.Field()  # Текущее время в формате timestamp
    RPC = scrapy.Field()  # {str} Уникальный код товара - есть в ссылке на товар.
    url = scrapy.Field()  # {str} Ссылка на страницу товара
    title = scrapy.Field()  # {str} Заголовок/название товара (если в карточке товара указан цвет или объем, необходимо добавить их в title в формате {название}, {цвет})
    marketing_tags = scrapy.Field(serializer=list)  # {list of str} Список тэгов, например ['Популярный', 'Акция', 'Подарок'], если тэг представлен в виде изображения собирать его не нужно
    brand = scrapy.Field()  # {str} Брэнд товара
    section = scrapy.Field(serializer=list)  # {list of str} Иерархия разделов, например ['Игрушки', 'Развивающие и интерактивные игрушки', 'Интерактивные игрушки']
    price_data = scrapy.Field(serializer=dict)
    original = scrapy.Field(serializer=float)  # {float} Оригинальная цена
    stock = scrapy.Field(serializer=dict)
    in_stock = scrapy.Field(serializer=bool)  # {bool} Должно отражать наличие товара в магазине
    count = scrapy.Field(serializer=int)  # {int} Если есть возможность получить информацию о количестве оставшегося товара в наличии, иначе 0
    assets = scrapy.Field(serializer=dict)
    main_image = scrapy.Field() # {str} Ссылка на основное изображение товара
    set_images = scrapy.Field(serializer=list)  # {list of str} Список больших изображений товара
    metadata = scrapy.Field(serializer=dict)
    __description = scrapy.Field()  # {str} Описание товар
    variants = scrapy.Field(serializer=int)  # {int} Кол-во вариантов у товара в карточке (За вариант считать только цвет или объем/масса. Размер у одежды или обуви варинтами не считаются)

## Apteka-Scrapy
Парсер для сбора данных c сайта apteka-ot-sklada.ru

## Технологии в проекте  
🔹 Python 
🔹 Scrapy
🔹 Proxy

## Подготовка и запуск проекта

1. Клонируйте репозиторий командой:
```bash
git clone git@github.com:oitczvovich/brandquad_parser_test.git
``` 

2. Активируйте venv и установите зависимости:

``` bash
python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt

```

### Настройки по умолчанию для работы без прокси.
3. 1. Внесите изменение в файле apteka_scrapy/settings.py. Параметры, которые настраиваются 
```python
# Ссылка на категории по которым необходимо провести парсинг
CATEGORY_BY_PARSING = [
    <Вставить сслыку на категорию типа "https://apteka-ot-sklada.ru/catalog/">
]
# Смотри ID городов на сайте  https://apteka-ot-sklada.ru/ 92 - соответсвует г.Томск,
PARSER_CITY_ID = "92" 
# время задержки запросов в секундах.
DOWNLOAD_DELAY = 1

```
### Настройка для работы с прокси.
3. 2. Настройки для работы с прокси.  

Создать файл .env
```bash
# через запятую указываем прокси, возможно использовать  прокси без аутентификации.
PROXY_LIST=host:posrt:login:password, host:posrt:login:password 
```

В файле apteka_scrapy/settings.py. Раскомментировать параметр. 
```bash
DOWNLOADER_MIDDLEWARES = {'apteka_scrapy.middlewares.HttpProxyMiddleware': 350,}
```
### Запуск парсера.

4. Запустите парсер из папки, где расположен файл README.md
```bash
scrapy crawl apteka_spider
```

5. Результаты сохраняются в папке results.
Изменить адрес сохранения результатов можно в apteka_scrapy/settings.py.
```bash
FEED_URI = <новые адрес и имя> 
```

В файл сохраняются следующие данные
```bash
    "city" - Для определения, из какой локации собраны данные.
    "timestamp" - Текущее время в формате timestamp
    "RPC" - Уникальный код товара - есть в ссылке на товар.
    "url" - Ссылка на страницу товара
    "title" - Заголовок/название товара (если в карточке товара указано количество в упаковке или объем, необходимо добавить их в title в формате {название}, {объем})
    "marketing_tags" - Список тэгов, например ['Популярный', 'Акция', 'Подарок'], если тэг представлен в виде изображения, собирать его не нужно
    "brand" - Бренд товара, берется из заголовка товара. Первое слово с большой буквы, если следующее слово тоже с большой буквы и также учитывается возможность предлога между словами.
    "section" -  Иерархия разделов, например ['Игрушки', 'Развивающие и интерактивные игрушки', 'Интерактивные игрушки']
    "price_data" 
    "original" - Оригинальная цена. Т.к. на сайте нет системы скидок, которую можно определить, брал цену, указанную на странице товара.

    "stock" = scrapy.Field(serializer=dict)
    "in_stock" - Отражать наличие товара в аптеках
    "count" - Если есть возможность получить информацию о количестве оставшегося товара в наличии, иначе 0
    "assets" 
    "main_image" - Ссылка на основное изображение товара
    "set_images" -  Список остальных изображений товара
    
    "metadata" 
    "__description" - Описание товара.
    Если у товара был в заголовке вес или количество в упаковке, указывается отдельно.
    "weight": "Вес", - сохраняется Вес и единица измерений. 
    "count": "Количество в упаковке", сохраняется как строка с N количество. 

    variants - на сайте у товара нет вариантов. По умолчанию везде 1.
```

## Авторы проекта
### Скалацкий Владимир
Telegramm: https://t.me/OitcZvovich<br>
e-mail: skalakcii@yandex.ru<br>
Github: https://github.com/oitczvovi<br>
Linkedin: https://www.linkedin.com/in/vladimirskala/<br>
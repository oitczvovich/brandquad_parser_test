from datetime import datetime


BOT_NAME = "apteka_scrapy"

SPIDER_MODULES = ["apteka_scrapy.spiders"]
NEWSPIDER_MODULE = "apteka_scrapy.spiders"

ITEM_PIPELINES = {'apteka_scrapy.pipelines.AptekaScrapyPipeline': 300}

# DOWNLOADER_MIDDLEWARES = {
#     'apteka_scrapy.middlewares.ProxyMiddleware': 325,
# }


# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:39.0) Gecko/20100101 Firefox/39.0'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"

# Название папки для сохранения результатов.
NOW_TIME = datetime.strftime(datetime.now(), '%Y.%m.%d-%H:%M')
FEED_URI = f'results/apteka_parser_{NOW_TIME}.json'
FEED_FORMAT = 'json'
FEED_EXPORTERS = {'json': 'scrapy.exporters.JsonItemExporter'}
FEED_EXPORT_ENCODING = 'utf-8'

# Смотри ID городов на сайте  https://apteka-ot-sklada.ru/
PARSER_CITY_ID = "92"
# 
CATEGORY_BY_PARSING = [
    "https://apteka-ot-sklada.ru/catalog/sredstva-gigieny/uhod-za-polostyu-rta/pasty-zubnye-vzroslym",
    "https://apteka-ot-sklada.ru/catalog/medikamenty-i-bady/vitaminy-i-mikroelementy/vitaminy-dlya-glaz",
    "https://apteka-ot-sklada.ru/catalog/hozyaystvennye-tovary/bytovaya-himiya",
]



# время задержки запросов 
DOWNLOAD_DELAY = 1


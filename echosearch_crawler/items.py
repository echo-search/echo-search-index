import scrapy

class EchosearchCrawlerItem(scrapy.Item):
    url = scrapy.Field()
    html = scrapy.Field()
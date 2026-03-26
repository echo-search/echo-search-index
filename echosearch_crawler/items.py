import scrapy

class EchosearchCrawlerItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    description = scrapy.Field()
    snippet = scrapy.Field()

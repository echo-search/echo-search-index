# Default Scrapy middlewares template

from scrapy import signals

class EchosearchCrawlerSpiderMiddleware:
    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def spider_opened(self, spider):
        spider.logger.info(f"Spider opened: {spider.name}")
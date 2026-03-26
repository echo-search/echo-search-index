import scrapy
from echosearch_crawler.items import EchosearchCrawlerItem

class EchoSpider(scrapy.Spider):
    name = "echo_spider"

    # Replace with safe seed URLs
    start_urls = [
        "https://wikipedia.org",
        "https://www.google.com",
        "https://echo-search.github.io"
    ]

    def parse(self, response):
        item = EchosearchCrawlerItem()
        item['url'] = response.url
        item['html'] = response.text
        yield item

        # Follow internal links only (optional)
        for href in response.css("a::attr(href)").getall():
            if href.startswith("http"):
                yield response.follow(href, self.parse)

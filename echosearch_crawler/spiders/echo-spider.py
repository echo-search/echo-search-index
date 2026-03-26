import scrapy
from echosearch_crawler.items import EchosearchCrawlerItem

class EchoSpider(scrapy.Spider):
    name = "echo_spider"

    # Safe, crawlable seeds — change later as you scale
    start_urls = [
        "https://www.wikipedia.org",
        "https://www.google.com",
        "https://www.bbc.co.uk",
        "https://echo-search.github.io",
        "https://jav-ai.netlify.app",
        "https://the-girl-gang.netlify.app",
        "https://github.com"
    ]

    def parse(self, response):
        item = EchosearchCrawlerItem()

        # --- Extract tiny, clean data (NOT full page) ---
        item['url'] = response.url
        item['title'] = response.xpath('//title/text()').get()

        item['description'] = response.xpath(
            '//meta[@name="description"]/@content'
        ).get()

        # first 500 characters of visible text (no HTML)
        snippet = ' '.join(response.xpath('//body//text()').getall())[:500]
        item['snippet'] = snippet

        yield item

        # --- Follow internal links only ---
        for href in response.css("a::attr(href)").getall():
            if href.startswith("http"):
                yield response.follow(href, self.parse)

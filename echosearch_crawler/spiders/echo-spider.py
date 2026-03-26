import scrapy
from echosearch_crawler.items import EchosearchCrawlerItem

class EchoSpider(scrapy.Spider):
    name = "echo_spider"

    # Safe, crawlable seeds — change later as you scale
    start_urls = [
    "https://en.wikipedia.org",
    "https://w3.org",
    "https://archive.org",
    "https://mozilla.org",
    "https://python.org",
    "https://gnu.org",
    "https://mit.edu",
    "https://harvard.edu",
    "https://stanford.edu",
    "https://berkeley.edu",
    "https://cornell.edu",
    "https://cam.ac.uk",
    "https://ox.ac.uk",
    "https://europa.eu",
    "https://un.org",
    "https://who.int",
    "https://worldbank.org",
    "https://weforum.org",
    "https://nasa.gov",
    "https://nih.gov",
    "https://noaa.gov",
    "https://github.io",
    "https://github.com",  # only public docs, many pages blocked
    "https://readthedocs.io",
    "https://deeplearning.ai",
    "https://tensorflow.org",
    "https://pytorch.org",
    "https://docs.python.org",
    "https://docs.github.com",
    "https://developer.mozilla.org",
    "https://boost.org",
    "https://kaggle.com",
    "https://echo-search.github.io"
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

BOT_NAME = "echosearch_crawler"

SPIDER_MODULES = ["echosearch_crawler.spiders"]
NEWSPIDER_MODULE = "echosearch_crawler.spiders"

ROBOTSTXT_OBEY = True
DOWNLOAD_DELAY = 1  # 1 second delay per request
CONCURRENT_REQUESTS_PER_DOMAIN = 1

# JSON output for GitHub Actions artifact
FEED_FORMAT = "json"
FEED_URI = "crawl_output.json"

# Pipeline placeholder (for future Step 4)
ITEM_PIPELINES = {
    'echosearch_crawler.pipelines.EchosearchCrawlerPipeline': 300,
}
BOT_NAME = "echosearch_crawler"

SPIDER_MODULES = ["echosearch_crawler.spiders"]
NEWSPIDER_MODULE = "echosearch_crawler.spiders"

# Respect robots.txt
ROBOTSTXT_OBEY = True

# --- SPEED & SAFETY ---
# Delay so you don’t hammer servers
DOWNLOAD_DELAY = 0.5

# Keep concurrency low to avoid slowdowns/timeouts
CONCURRENT_REQUESTS_PER_DOMAIN = 2

# Smart auto-throttle: speeds up when fast, slows down when slow
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 0.5
AUTOTHROTTLE_TARGET_CONCURRENCY = 3.0
AUTOTHROTTLE_MAX_DELAY = 10

# --- 6-HOUR LIFESAVER SETTINGS ---
# Hard stop after X pages (prevents GitHub Actions 6hr failure)
CLOSESPIDER_PAGECOUNT = 1000000

# Hard stop after ~5.5 hours (backup safety)
CLOSESPIDER_TIMEOUT = 10800   # seconds (5.5 hours)

# --- FEED OUTPUT ---
FEED_FORMAT = "json"
FEED_URI = "crawl_output.json"

ITEM_PIPELINES = {
    'echosearch_crawler.pipelines.DedupPipeline': 200,
    'echosearch_crawler.pipelines.ElasticsearchPipeline': 300,
}

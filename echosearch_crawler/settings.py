BOT_NAME = "echosearch_crawler"

SPIDER_MODULES = ["echosearch_crawler.spiders"]
NEWSPIDER_MODULE = "echosearch_crawler.spiders"

# -----------------------------
# RESPECT ROBOTS.TXT
# -----------------------------
ROBOTSTXT_OBEY = True

# -----------------------------
# SPEED + SAFETY
# -----------------------------
DOWNLOAD_DELAY = 0.5
CONCURRENT_REQUESTS_PER_DOMAIN = 2

AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 0.5
AUTOTHROTTLE_TARGET_CONCURRENCY = 3.0
AUTOTHROTTLE_MAX_DELAY = 10

# -----------------------------
# PREVENT 6-HR GITHUB CANCELLATION
# -----------------------------
CLOSESPIDER_PAGECOUNT = 100    # you can change this
CLOSESPIDER_TIMEOUT = 20701         # ~5.5 hours

# -----------------------------
# PIPELINES (ES + DEDUP)
# -----------------------------
ITEM_PIPELINES = {
    'echosearch_crawler.pipelines.DedupPipeline': 200,
}

# -----------------------------
# DISABLE FEED OUTPUT (IMPORTANT)
# -----------------------------
FEEDS = {
    'crawl_output.json': {
        'format': 'json',
        'encoding': 'utf8',
        'indent': 0,
        'overwrite': True,
    }
}

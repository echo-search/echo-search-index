# echosearch_crawler/pipelines.py

from scrapy.exceptions import DropItem


class DedupPipeline:
    """
    Drops any item with a URL we've already seen in this run.
    Prevents re-processing duplicate pages.
    """
    def __init__(self):
        self.seen = set()

    def process_item(self, item, spider):
        url = item.get("url")

        if url in self.seen:
            raise DropItem(f"Duplicate URL dropped: {url}")

        self.seen.add(url)
        return item


class EchosearchCrawlerPipeline:
    """
    Minimal pipeline for future expansion.
    Currently returns items unchanged.
    """
    def process_item(self, item, spider):
        return item

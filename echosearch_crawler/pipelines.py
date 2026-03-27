# echosearch_crawler/pipelines.py

from scrapy.exceptions import DropItem
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk


class DedupPipeline:
    """
    Drops any item with a URL we've already seen in this run.
    Prevents processing the same page twice.
    """
    def __init__(self):
        self.seen = set()

    def process_item(self, item, spider):
        url = item.get("url")
        if not url:
            raise DropItem("Missing URL field")

        if url in self.seen:
            raise DropItem(f"Duplicate URL dropped: {url}")

        self.seen.add(url)
        return item


class ElasticsearchPipeline:
    """
    Sends items directly into Elasticsearch.
    No JSON files. No GitHub storage. Fast + clean.
    """
    def __init__(self):
        # connect to ES running in Codespaces/Docker
        self.es = Elasticsearch("http://localhost:9200", verify_certs=False)
        self.actions = []

    def process_item(self, item, spider):
        # Prepare an ES bulk operation
        action = {
            "_index": "echosearch",
            "_source": dict(item)
        }
        self.actions.append(action)

        # Flush in batches of 1000
        if len(self.actions) >= 1000:
            bulk(self.es, self.actions)
            self.actions.clear()

        return item

    def close_spider(self, spider):
        # Final flush when spider ends
        if self.actions:
            bulk(self.es, self.actions)
            self.actions.clear()

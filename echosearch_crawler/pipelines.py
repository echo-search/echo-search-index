# Minimal pipelines template
# We aren't storing anything extra yet; pipeline exists for future parsing/indexing

class EchosearchCrawlerPipeline:
    def process_item(self, item, spider):
        return item
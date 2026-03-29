import json
from elasticsearch import Elasticsearch, helpers

es = Elasticsearch("http://localhost:9200")
index_name = "echoindex"

with open("crawl_output.json") as f:
    data = json.load(f)

actions = []

for item in data:
    actions.append({
        "_index": index_name,
        "_source": item
    })

helpers.bulk(es, actions)
print("Done! Indexed:", len(actions), "items")
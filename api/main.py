from fastapi import FastAPI, Query
from elasticsearch import Elasticsearch

app = FastAPI()
es = Elasticsearch("http://localhost:9200")
index_name = "echoindex"

@app.get("/search")
def search(q: str = Query(...)):
    resp = es.search(
        index=index_name,
        query={
            "multi_match": {
                "query": q,
                "fields": ["title^3", "description^2", "snippet"]
            }
        }
    )

    hits = [
        {
            "url": hit["_source"]["url"],
            "title": hit["_source"]["title"],
            "description": hit["_source"]["description"],
        }
        for hit in resp["hits"]["hits"]
    ]

    return {"results": hits}
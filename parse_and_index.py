import json
import re
from bs4 import BeautifulSoup
from elasticsearch import Elasticsearch, helpers

# Elasticsearch connection
es = Elasticsearch("https://407f6567cff94b42a621cb81c626064c.europe-west2.gcp.elastic-cloud.com:443", basic_auth=("USER", "PASS"))

# Load the crawl JSON
with open("crawl_output.json", "r", encoding="utf-8") as f:
    crawl_data = json.load(f)

def clean_text(html):
    soup = BeautifulSoup(html, "lxml")

    # remove scripts and styles
    for script in soup(["script", "style", "nav", "footer", "header"]):
        script.decompose()

    # get visible text
    text = soup.get_text(separator=" ", strip=True)
    # collapse multiple spaces
    text = re.sub(r"\s+", " ", text)
    return text

def extract_snippet(text, length=200):
    return text[:length] + "…" if len(text) > length else text

# Prepare bulk docs for Elasticsearch
actions = []
for page in crawl_data:
    url = page["url"]
    html = page["html"]

    text = clean_text(html)
    snippet = extract_snippet(text)
    title_tag = BeautifulSoup(html, "lxml").title
    title = title_tag.string.strip() if title_tag and title_tag.string else ""
    
    # Optional meta description
    meta_desc_tag = BeautifulSoup(html, "lxml").find("meta", attrs={"name": "description"})
    description = meta_desc_tag["content"].strip() if meta_desc_tag else snippet

    doc = {
        "_index": "echosearch",
        "_id": url,  # use URL as unique ID
        "_source": {
            "url": url,
            "title": title,
            "description": description,
            "snippet": snippet
        }
    }
    actions.append(doc)

# Bulk index to Elasticsearch
helpers.bulk(es, actions)
print(f"Indexed {len(actions)} documents to Elasticsearch")

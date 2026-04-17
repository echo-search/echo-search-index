import requests
import gzip
import json
import os

BASE_URL = "https://data.commoncrawl.org/"
BATCH_FILE = "batch.txt"
OUTPUT_FILE = "public/index.json"
MAX_DOCS = 99999999999


def parse_wet_file(url):
    docs = []

    try:
        response = requests.get(url, stream=True, timeout=20)
        gz = gzip.GzipFile(fileobj=response.raw)

        content = gz.read().decode("utf-8", errors="ignore")
        blocks = content.split("WARC/1.0")

        for block in blocks:
            if "WARC-Type: conversion" not in block:
                continue

            try:
                url_line = block.split("WARC-Target-URI: ")[1].split("\n")[0]
                text = block.split("\n\n", 1)[1].strip()

                docs.append({
                    "url": url_line,
                    "title": text[:80],
                    "description": text[:160],
                    "snippet": text[:200]
                })

            except Exception:
                continue

    except Exception as e:
        print("Error:", url, e)

    return docs


def main():
    all_docs = []

    with open(BATCH_FILE) as f:
        paths = [line.strip() for line in f.readlines()]

    for path in paths:
        full_url = BASE_URL + path
        print("Processing:", full_url)

        docs = parse_wet_file(full_url)
        all_docs.extend(docs)

    os.makedirs("public", exist_ok=True)

    if os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE) as f:
            existing = json.load(f)
    else:
        existing = []

    combined = existing + all_docs

    # prevent repo from exploding
    combined = combined[-MAX_DOCS:]

    with open(OUTPUT_FILE, "w") as f:
        json.dump(combined, f)


if __name__ == "__main__":
    main()

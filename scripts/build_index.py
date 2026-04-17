import requests
import gzip
import json
import os
import glob

BASE_URL = "https://data.commoncrawl.org/"
OUTPUT_FILE = "public/index.json"
MAX_DOCS = 100000  # be realistic or GitHub will cry


def parse_wet_stream(url):
    try:
        response = requests.get(url, stream=True, timeout=30)
        response.raise_for_status()

        gz = gzip.GzipFile(fileobj=response.raw)

        buffer = ""
        for chunk in gz:
            buffer += chunk.decode("utf-8", errors="ignore")

            while "WARC/1.0" in buffer:
                part, buffer = buffer.split("WARC/1.0", 1)

                if "WARC-Type: conversion" not in part:
                    continue

                try:
                    url_line = part.split("WARC-Target-URI: ")[1].split("\n")[0]
                    text = part.split("\n\n", 1)[1].strip()

                    yield {
                        "url": url_line,
                        "title": text[:80],
                        "description": text[:160],
                        "snippet": text[:200]
                    }

                except Exception:
                    continue

    except Exception as e:
        print("Error:", url, e)


def get_batch_files():
    # supports both split batches and single file
    files = sorted(glob.glob("batch_*"))

    if files:
        return files
    elif os.path.exists("batch.txt"):
        return ["batch.txt"]
    else:
        raise FileNotFoundError("No batch files found")


def main():
    os.makedirs("public", exist_ok=True)

    # load existing index safely
    if os.path.exists(OUTPUT_FILE):
        try:
            with open(OUTPUT_FILE) as f:
                combined = json.load(f)
        except:
            combined = []
    else:
        combined = []

    batch_files = get_batch_files()

    for batch_file in batch_files:
        print("Using batch:", batch_file)

        with open(batch_file) as f:
            paths = [line.strip() for line in f if line.strip()]

        for path in paths:
            full_url = BASE_URL + path
            print("Processing:", full_url)

            for doc in parse_wet_stream(full_url):
                combined.append(doc)

                # keep size under control
                if len(combined) > MAX_DOCS:
                    combined = combined[-MAX_DOCS:]

    # write once at the end
    with open(OUTPUT_FILE, "w") as f:
        json.dump(combined, f)

    print("Done. Total docs:", len(combined))


if __name__ == "__main__":
    main()

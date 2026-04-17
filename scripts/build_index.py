import requests
import gzip
import json
import os
import glob
from bs4 import BeautifulSoup

BASE_URL = "https://data.commoncrawl.org/"
OUTPUT_FILE = "public/index.json"
MAX_DOCS = 100000


def extract_html_fields(html):
    soup = BeautifulSoup(html, "html.parser")

    # title
    title_tag = soup.find("title")
    title = title_tag.get_text(strip=True) if title_tag else None

    # meta description
    desc_tag = soup.find("meta", attrs={"name": "description"})
    if not desc_tag:
        desc_tag = soup.find("meta", attrs={"property": "og:description"})

    description = desc_tag["content"].strip() if desc_tag and desc_tag.get("content") else None

    # fallback text
    text = soup.get_text(separator=" ", strip=True)

    return title, description, text


def parse_warc_stream(url):
    try:
        response = requests.get(url, stream=True, timeout=30)
        response.raise_for_status()

        gz = gzip.GzipFile(fileobj=response.raw)

        buffer = ""

        for chunk in gz:
            buffer += chunk.decode("utf-8", errors="ignore")

            while "WARC/1.0" in buffer:
                part, buffer = buffer.split("WARC/1.0", 1)

                if "Content-Type: text/html" not in part:
                    continue

                try:
                    target_url = part.split("WARC-Target-URI: ")[1].split("\n")[0]
                    html = part.split("\r\n\r\n", 1)[1]

                    title, description, text = extract_html_fields(html)

                    yield {
                        "url": target_url,
                        "title": title or text[:80],
                        "description": description or text[:160],
                        "snippet": text[:200]
                    }

                except Exception:
                    continue

    except Exception as e:
        print("Error:", url, e)


def get_batch_files():
    files = sorted(glob.glob("batch_*"))
    if files:
        return files
    elif os.path.exists("batch.txt"):
        return ["batch.txt"]
    else:
        raise FileNotFoundError("No batch files found")


def main():
    os.makedirs("public", exist_ok=True)

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

            for doc in parse_warc_stream(full_url):
                combined.append(doc)

                if len(combined) > MAX_DOCS:
                    combined = combined[-MAX_DOCS:]

    with open(OUTPUT_FILE, "w") as f:
        json.dump(combined, f)

    print("Done. Docs:", len(combined))


if __name__ == "__main__":
    main()

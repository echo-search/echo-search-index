#!/bin/bash

curl -X PUT "http://localhost:9200/echosearch" \
  -H "Content-Type: application/json" \
  -d '{
    "mappings": {
      "properties": {
        "url":        { "type": "keyword" },
        "title":      { "type": "text" },
        "description":{ "type": "text" },
        "content":    { "type": "text" },
        "timestamp":  { "type": "date" }
      }
    }
  }'

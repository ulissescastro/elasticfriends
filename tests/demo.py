#!/usr/bin/env python
import elasticsearch

# Connect to localhost:9200 by default:
es = elasticsearch.Elasticsearch()

# Round-robin between two nodes:
es = elasticsearch.Elasticsearch(["localhost:9200"])

# Connect to cluster at search1:9200, sniff all nodes and round-robin between them
es = elasticsearch.Elasticsearch(["localhost:9200"], sniff_on_start=True)

# Index a document:
es.index(
    index="my_app",
    doc_type="blog_post",
    id=1,
    body={
        "title": "Elasticsearch clients",
        "content": "Interesting content...",
        "date": date(2013, 9, 24),
    }
)

# Get the document:
es.get(index="my_app", doc_type="blog_post", id=1)

# Search:
 es.search(index="my_app", body={"query": {"match": {"title": "elasticsearch"}}})


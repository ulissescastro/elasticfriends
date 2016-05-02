#!/usr/bin/env python
import elasticsearch
import sys

# Connect to localhost:9200 by default:
es = elasticsearch.Elasticsearch()

# Round-robin between two nodes:
#es = elasticsearch.Elasticsearch(["localhost:9200"])

# Connect to cluster at search1:9200, sniff all nodes and round-robin between them
#es = elasticsearch.Elasticsearch(["localhost:9200"], sniff_on_start=True)

# Index a document:
#es.index(
#    index="my_app",
#    doc_type="blog_post",
#    id=1,
#    body={
#        "title": "Elasticsearch clients",
#        "content": "Interesting content...",
#        "date": date(2013, 9, 24),
#    }
#)

# Get the document:
#es.get(index="xxxmy_app", doc_type="blog_post", id=1)

# Search:
r = es.search(index="demo", body={
  "query": {
    "filtered": {
      "query": {
        "bool": {
          "should": [
            {
              "query_string": {
                "query": "%s" % sys.argv[1]
              }
            }
          ]
        }
      },
      "filter": {
        "bool": {
          "must_not": [
            {
              "fquery": {
                "query": {
                  "query_string": {
                    "query": "plaintext:[\"\" TO *]"
                  }
                },
                "_cache": 'true'
              }
            }
          ]
        }
      }
    }
  },
  "highlight": {
    "fields": {},
    "fragment_size": 2147483647,
    "pre_tags": [
      "@start-highlight@"
    ],
    "post_tags": [
      "@end-highlight@"
    ]
  },
  "size": 500,
  "sort": [
    {
      "plaintext": {
        "order": "asc"
      }
    }
  ]
})

for i in r.iteritems():
    try:
        for j in i[1]['hits']:
            print "%s:%s" % (j['_source']['hash'], j['_source']['plaintext'])
    except:
        pass


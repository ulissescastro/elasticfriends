#!/usr/bin/env python
import elasticsearch
import sys
import json


# Connect to localhost:9200
es = elasticsearch.Elasticsearch()

# Get the document:
#print es.get(index="mxyzptlk", doc_type="metadata", sha1="fa931241fc50b592dec0468b707cfc627671f920")

result = es.search(
        index = "mxyzptlk",
        body = {
            "query": {
                "match": {
                    str(sys.argv[1]): str(sys.argv[2])
                    }
                }
            }
        )

print json.dumps(result, indent=4)
#print parsed
#print json.dumps(parsed, indent=4, sort_keys=False)


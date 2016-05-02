#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import elasticsearch

# Create and populate function
def populate(es, md5_hash, md5_plain):
    es.index(
            index = "md5",
            doc_type = 'hashes',
            body = {
                "hash": md5_hash,
                "plaintext": md5_plain,
                },
            )
    return

# Connect to localhost:9200
es = elasticsearch.Elasticsearch()
line = str(sys.argv[1])
md5_hash, md5_plain = line.split(':', 1)
populate(es, md5_hash.lower(), md5_plain)

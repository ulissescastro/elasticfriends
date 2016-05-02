#!/usr/bin/env python
# -*- coding: utf-8 -*-
import elasticsearch
import sys

# Connect to localhost:9200
es = elasticsearch.Elasticsearch()

es.index(
        index = "ownage",
        doc_type = "metadata",
        id=
        body = {
            "name": "gilson xxxx leite",
            "email": "gilson.xman@hotmail.com",
            "md5": "e745de87439175616094e568ea783548",
            "plaintext": "nayara",
            }
        )


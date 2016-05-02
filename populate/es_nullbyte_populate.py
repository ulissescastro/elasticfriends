#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import re
import elasticsearch
from BeautifulSoup import BeautifulStoneSoup

# Create and populate function
def populate(es, md5_hash, md5_plain):
    es.index(
            index = "demo",
            doc_type = 'nullbyte',
            body = {
                "hash": md5_hash,
                "plaintext": md5_plain,
                },
            )
    return

# Connect to localhost:9200
es = elasticsearch.Elasticsearch()

# Read potfile
data = open(sys.argv[1]).readlines()
total = len(data)

count = 0
while data:
    line = data.pop(0).replace('\n', '')
    md5_hash, md5_plain = line.split(':', 1)
    populate(es, md5_hash.lower(), md5_plain)
    count += 1
    if 100 % count == 100:
        p = 100 * float(count)/float(total)
        os.system('clear')        
        print "progress: %s" % str(p)[:4]

    #print "%s %s" % (md5_hash, md5_plain)

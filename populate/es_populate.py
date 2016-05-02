#!/usr/bin/env python
# -*- coding: utf-8 -*-
import elasticsearch
import sys
import csv
from BeautifulSoup import BeautifulStoneSoup

def populate(es, name, email, plaintext, source, database, table_name):
    es.index(
            index = "ownage",
            doc_type = source,
            body = {
                "name": name,
                "email": email,
                "plaintext": plaintext,
                "database": database,
                "table_name": table_name,
                },
            )
    return


# Connect to localhost:9200
es = elasticsearch.Elasticsearch()

source = str(sys.argv[1])
database = str(sys.argv[2])
table_name = str(sys.argv[3])

reader = csv.reader(sys.stdin)

for line in reader:
    name = str(BeautifulStoneSoup(line[0], convertEntities=BeautifulStoneSoup.HTML_ENTITIES))
    email = str(BeautifulStoneSoup(line[1], convertEntities=BeautifulStoneSoup.HTML_ENTITIES))
    plaintext = str(line[2])
    populate(es, name.lower().strip().title(), email.lower(), plaintext, source, database, table_name)
    print "%s %s %s %s %s %s" % (name.lower().strip().title(), email.lower(), plaintext, source, database, table_name)

    

#!/usr/bin/env python
# -*- coding: utf-8 -*-
import elasticsearch
import sys
import csv
from BeautifulSoup import BeautifulStoneSoup
from hashlib import md5
from zlib import adler32
import unicodedata
import uuid

def create_hash_id(keyword_row):
    m = md5()
    m.update(str(keyword_row))
    return uuid.uuid4(m.hexdigest())

def es_insert(es, index, doc_type, keyword_row):
    id_hash = create_hash_id(keyword_row)
    #id_hash = adler32(str(keyword_row))
    # es.get(index=index, doc_type=doc_type, id=id_hash)
    es.index(
            index = index,
            doc_type = doc_type,
            id = id_hash,
            body = keyword_row,
            )

    return

def sanitize(string):
    try:
        string = string.strip()
        string = unicode(string, 'latin-1')
        string = unicodedata.normalize('NFKD', string).encode('ascii', 'ignore')
        string = string.lower()
    except Exception, e:
        print "[%s] sanitize error: %s" % (string, e)
        pass

    return string


if __name__ == "__main__":
    # sqlite3 -header -nullvalue 'NULL' -csv <sqlite3 file> "select * from table" | csv2elasticsearch.py <index> <doc_type>

    # Connect to localhost:9200
    es = elasticsearch.Elasticsearch()

    #index = str(sys.argv[1])
    index = "elasticfriends"
    doc_type = str(sys.argv[1])
    keyword_row = {}

    reader = csv.reader(sys.stdin)

    rownum = 0
    for row in reader:
        if rownum == 0:
            header = row
            header_length = len(header)
        else:
            #colnum = 0
            for col in range(0, header_length):
            #while row:
                collumn_data = row[col]
                #keyword_row[header[colnum]] = sanitize(col)
                keyword_row[header[col]] = sanitize(collumn_data)
                #print '%-8s: %s' % (header[colnum], col)
                #colnum +=1
            
            if len(keyword_row) != header_length:
                print "something went wrong: %s" % str(keyword_row)
            
            es_insert(es, index, doc_type, keyword_row)

        rownum += 1



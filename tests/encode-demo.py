#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, elasticsearch
from hashlib import md5


def hash_it(string):
    m = md5()
    m.update(string)
    return m.hexdigest()


def es_insert(es, pw_hash, pw_plain):
#def es_insert(es):
    result = es.index(
            index = "elasticfriends",
            doc_type = "test",
            body = { "hash": pw_hash, "plain": pw_plain },
            #body = { "hash": "8f22a04a84c45e20d2021e6e93156f78", "plain": "Guimarães" },
            )
    
    return result

es = elasticsearch.Elasticsearch()

pw_hex = str(sys.argv[1])
pw_plain = pw_hex.decode('hex')
pw_hash = hash_it(pw_plain)
print "pw_hex:%s\tpw_plain:%s\tpw_hash:%s" % (pw_hex, pw_plain, pw_hash)

print es_insert(es, pw_hash, pw_plain)
#print es_insert(es)


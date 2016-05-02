#!/usr/bin/env python
# -*- coding: utf-8 -*-
import elasticsearch
import sys
import csv
from hashlib import md5
import unicodedata
import uuid
from BeautifulSoup import BeautifulStoneSoup


def hash_it(string):
    m = md5()
    m.update(string)
    return m.hexdigest()


def create_hash_id(keyword_row):
    id_hash = hash_it(str(keyword_row))
    return uuid.UUID(id_hash)


def es_insert(es, index, doc_type, keyword_row):
    id_hash = create_hash_id(keyword_row)
    r = es.index(
            index = index,
            doc_type = doc_type,
            id = id_hash,
            body = keyword_row,
            )

    return r

def es_insert_garbage(es, index, doc_type, keyword_row):
    id_hash = create_hash_id(keyword_row)
    doc_type = "%s-garbage" % doc_type
    r = es.index(
            index = index,
            doc_type = doc_type,
            id = id_hash,
            body = keyword_row,
            )
    
    return r


def sanitize(string):
    if len(string) == 0:
        return ''

    try:
        string = string.replace('\n','')
        string = unicode(string, 'latin-1')
        string = unicodedata.normalize('NFKD', string).encode('ascii', 'ignore')
        string = string.strip()
        string = ' '.join(string.split(' '))
        string = string.lower()
    except Exception, e:
        print "[%s] sanitize error: %s" % (string, e)
        pass

    return string


def sanitize_name(string):
    if len(string) > 0 and string.lower() != "null":
        try:
            string = string.decode('hex')
        except Exception, e:
            print "[%s] %s" % (string, e)
            sys.exit(0)
    elif string.lower() == "null":
            string = ''

    return sanitize(string).title()


def sanitize_password_hash(keyword_row):
    # decode hex to plain to avoid problems with special chars @ cmd line
    if len(keyword_row['password_cracked']) > 0:
        try:
            keyword_row['password_cracked'] = keyword_row['password_cracked'].decode('hex')
        except Exception, e:
            #print "[error] password_cracked hex decode\n%s\n%s" % (keyword_row['password_cracked'], e)
            sys.exit(0)

    pw_hash_len = len(keyword_row['password_hash'])
    pw_cracked_len = len(keyword_row['password_cracked'])

    if pw_hash_len == 0 and pw_cracked_len > 1:
        keyword_row['password_hash'] = hash_it(keyword_row['password_cracked'])
        #print "[hashing] %s as %s" % (keyword_row['password_cracked'], keyword_row['password_hash'])

    return keyword_row


def sanitize_email(keyword_row):
    if len(keyword_row['email']) == 0:
        keyword_row['email'] = ''

    if "@" not in keyword_row['email']:
        return False

    sanitized_email = sanitize(keyword_row['email'])
    if " " in sanitized_email:
        return False
    
    keyword_row['email'] = sanitized_email
    
    return keyword_row


if __name__ == "__main__":

    # Connect to localhost:9200
    es = elasticsearch.Elasticsearch()

    index = "elasticfriends"
    doc_type = str(sys.argv[2])
    table_name = sanitize(str(sys.argv[3]))
    keyword_row = {}
    counter = 0

    reader = csv.reader(open(str(sys.argv[1]), 'rb').readlines())

    rownum = 0
    for row in reader:
        if rownum == 0:
            header = row
            header_length = len(header)
            #print "%s %s" % (header_length, header)
        else:
            colnum = 0
            for column_data in row:
                column_name = header[colnum]
                if column_name == "name":
                    column_data = sanitize_name(column_data)

                keyword_row[column_name] = column_data
                colnum += 1
            

            keyword_row = sanitize_password_hash(keyword_row)

            keyword_row['table'] = table_name
            
            if not sanitize_email(keyword_row):
                #print "[garbage] %s" % str(keyword_row)
                es_insert_garbage(es, index, doc_type, keyword_row)
                continue

            es_insert(es, index, doc_type, keyword_row)
            counter += 1

        rownum += 1

    print "Done, %s line(s) imported." % counter



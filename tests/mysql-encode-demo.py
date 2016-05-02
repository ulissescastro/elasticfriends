#!/usr/bin/python
# -*- coding: utf-8 -*-
#import MySQLdb
import sqlite3

dbs = sqlite3.connect('/tmp/dbtest.sqlite3')

#db = MySQLdb.connect(host="localhost", # your host, usually localhost
#                     user="root", # your username
#                      passwd="toor", # your password
#                      db="dummy") # name of the data base

# you must create a Cursor object. It will let
#  you execute all the queries you need
#cur = db.cursor() 
sqcur = dbs.cursor()

# Use all the SQL you like
#cur.execute("select hex(convert(senha using utf8)) from usuario where senha like 'Gui%'")
sqcur.execute("select nome,senha,login,email,homepage from usuario")

# print all the first cell of all the rows
decoderow = []
for row in sqcur.fetchall():
    for col in row:
        if 'blank' in col or 'NULL' in col:
            continue
        else:
            decoderow.append(col.decode('hex'))
    print decoderow
    decoderow = []



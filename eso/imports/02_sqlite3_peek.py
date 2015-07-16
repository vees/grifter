# -*- coding: utf-8 -*-
"""
Created on Mon Jul 13 13:55:21 2015

@author: rob
"""

'''
This script also seemed useful although I didn't need something
quite as complicated as it:
https://pagehalffull.wordpress.com/2012/11/14/python-script-to-count-tables-columns-and-rows-in-sqlite-database/
'''

'''Of interest:
/home/rob
./url.db
./mailmaker.db
./hangnail/bcps/bcps.db
./Projects/dupfiles/files.db
./Projects/dupfiles/example.db
/media/dev/projects
./poptart/urls.db
./narthex/narthex-dev.db
./narthex/grifter.db
'''

import sqlite3
conn=sqlite3.connect('/media/dev/projects/narthex/narthex-dev.db')
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tableList=  cursor.fetchall()
tableList[0][0]
for table in tableList:
    rowsQuery = "SELECT Count() FROM %s" % table[0]
    none = cursor.execute(rowsQuery)
    numberOfRows = cursor.fetchone()[0]
    if numberOfRows != 0:
        print table[0],numberOfRows

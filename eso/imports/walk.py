# -*- coding: utf-8 -*-
"""
Created on Sat Jul  4 09:23:28 2015

@author: rob
"""

import os
from datetime import datetime

def get_stat_hash(filename):
    '''Given a filename, returns a unique value for its state
    on the filesystem. If any attribute of the file were to
    change this number would also change'''
    statinfo = os.stat(filename)
    return statinfo.__hash__()

def get_stat_size(filename):
    statsize = os.path.getsize(filename)
    return statsize

def files_under_dir(dirname):
    '''Great example from http://stackoverflow.com/a/2186565/682915'''
    matches = []
    for root, dirnames, filenames in os.walk(dirname):
        for filename in filenames:
            matches.append(os.path.join(root, filename))
    return matches

def files_and_stat(files):
    return [(filename,get_stat_hash(filename),get_stat_size(filename)) 
        for filename in files]

if __name__ == "__main__":
    '''This function demonstrates that 50k files run in about 15
    seconds on my shitty laptop and if you run it and continue
    the interpreter you'll get a list of all the files and 
    signed integer representing each'''
    start = datetime.now()
    foo = files_and_stat(files_under_dir("/media/dev/photos"))
    end = datetime.now()
    print end-start
    print len(foo)

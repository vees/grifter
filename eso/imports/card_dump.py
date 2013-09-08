import os
import glob
import itertools
import hashlib
from datetime import datetime
from django.conf import settings

from exo.models import Picture, Moment, PictureSimple

def compare_md5_file(filename):
    f = open(filename, 'r')
    already_matched=0
    for line in f:
        (md5,path)=line.split()
        count = PictureSimple.objects.filter(file_hash=md5).count()
        if count==0:
            print "No match found, import %s" % path
        elif count==1:
            already_matched += 1
            #print "Match found, skipping"
        elif count>1:
            print "WARNING: Multiple matches in database already"
        else:
            print "WARNING: Nothing matched"
    print "Files already matched: %s" % already_matched

def main():
    """Import images from the default path"""
    try:
        print compare_md5_file('/home/rob/cardsrun/3819407463.txt')
    except KeyboardInterrupt:
        print "Done."
        exit

if __name__ == '__main__':
    main()


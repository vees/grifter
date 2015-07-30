# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 21:33:48 2015

@author: rob
"""

import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "exo.settings")
django.setup()

from eso.imports import walk
from exo.models import ContentInstance, ContentContainer, ContentSignature


def walk_card(path):
    # /media/rob/3838-3431
    # 43 minutes 43 seconds for 50347 records
    from datetime import datetime
    start = datetime.now()
    walked = walk.file_dir_stat_size(path)
    end = datetime.now()
    duration = end-start
    print duration
    return walked

def data_load(walked, server, drive, path):
    #server="love", drive="8909006990", path='/Volumes/8909006990'
    n=0
    c, created = ContentContainer.objects.get_or_create(
        server=server, drive=drive, path=path)
    for walkunit in walked:
        n+=1
        if (n % 1000 == 0):
            print n
        cs, createds = ContentSignature.objects.get_or_create(
            md5=walkunit[6], sha2=walkunit[7], 
            content_size=walkunit[5])
        ci, createdi = ContentInstance.objects.get_or_create(
            filename = walkunit[2],
            content_container = c,
            relpath=walkunit[3],
            stat_hash=walkunit[4],
            content_signature=cs)
        print "Sig",createds,"Instance", createdi,walkunit[2]


# 8909006990  990 imported
# 905 empty
# 365 empty
# 3838-3431 431  caitlin's old phone - imported
#  b6f linux distro - can be formatted
# 5500392008  008 empty
# 2668872787 787 imported along with spotlight crap to ID and remove
# 1473001575 575 imported with spotlight crap
# 9387033553 553 empty 
# 876F-D108 108  old android backup, archive folder from main drive, lots of stuff, imported
# 132 1996691132 pictures loaded
# 65e 265A-465E pictures loaded
# 9900773857 857 empty
# EURO1 ireland photos

def cardload(drivename):
    walked=walk_card('/Volumes/'+drivename)
    data_load(walked,'love','304','/Volumes/'+drivename)

cardload('Miscellany')

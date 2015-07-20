# -*- coding: utf-8 -*-
"""
Created on Wed Jul 15 14:23:31 2015

@author: rob
"""

import csv
with open('/home/rob/Dropbox/With Work/photo_md5.csv', 'rb') as photomd5:
    photomd5reader = csv.reader(photomd5, delimiter=',', quotechar='"')
    for row in photomd5reader:
        print row[0], row[1]

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "exo.settings")
import django
django.setup()

from exo.models import ContentInstance, ContentContainer, ContentSignature, ContentKey

# Find something on this server we can play with
ContentInstance.objects.exclude(content_container=2).last()
ContentInstance._meta.fields[0].name
b=ContentInstance._meta.fields[0]
b.name
getattr(b,'name')

import exo.models
reload(exo.models)
from exo.models import Picture

Picture.objects.all()
from PIL import Image

#
# Import CSV  photo_md5 with format
# 0 ID, 1 md5, 2 path, 3 rating, 4 taken on date, 5 rotation
# See if there's a match to the MD5 (there may be multiple matches)
# Add fields to Picture
# Save
#

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "exo.settings")
import django
django.setup()


from exo.models import ContentInstance, ContentContainer, ContentSignature, ContentKey, Picture

cs=ContentSignature.objects.filter(md5='a120875a769b68cc35ffee887b9b82d0')
ci=cs.first().contentinstance_set.first()
ci.content_container.path,ci.relpath,ci.filename
"/".join((ci.content_container.path,ci.relpath,ci.filename))

no_match=[]
import csv
from PIL import Image
with open('photo_md5.csv', 'rb') as photomd5:
    photomd5reader = csv.reader(photomd5, delimiter=',', quotechar='"')
    for row in photomd5reader:
        if int(row[0]) < 29234:
            continue
        print row[0], row[1]
        signatures = ContentSignature.objects.filter(md5=row[1])
        for sig in signatures:
            ci=sig.contentinstance_set.first()
            if Picture.objects.filter(signature=sig).count() == 1:
                continue
            fileloc="/".join((ci.content_container.path,ci.relpath,ci.filename))
            try:
                i=Image.open(fileloc)
            except IOError:
                continue
            Picture.objects.get_or_create(
                signature=sig, defaults={
                'rotation': row[5],
                'width': i.size[0],
                'height': i.size[1],
                'rating': row[3],
                'taken_on': row[4]})      
                
from django.db import connection; connection.close()

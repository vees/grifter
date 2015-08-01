# -*- coding: utf-8 -*-
"""
Created on Sat Aug  1 18:56:25 2015

@author: rob
"""

import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "exo.settings")
django.setup()

from eso.imports import walk
from exo.models import ContentInstance, ContentContainer, ContentSignature, Tag2

from django.db import connection; connection.close()

#
# Lets do some experiments
#

# How many MP3 files do we have

ContentInstance.objects.filter(filename__endswith='.mp3').count()
# 4723

# Are there any content signatures where the filenames are different?
# ContentSignature - ContentInstance Set - count unique filename

from django.db.models import Count
ContentSignature.objects.annotate(unique_file=Count('contentinstance__filename',distinct=True)).filter(unique_file__gt=2).count()
# 3261
ContentSignature.objects.annotate(unique_file=Count('contentinstance__filename',distinct=True)).filter(unique_file=2).count()
# 3100
instances = ContentSignature.objects.annotate(unique_file=Count('contentinstance__filename',distinct=True)).filter(unique_file=3).first().contentinstance_set.all()
["/".join([x.relpath,x.filename]) for x in instances]
#[u'sd600-20080702/IMG_7798.JPG', 
# u'sd600-20080702/IMG_7798.JPG', 
# u'Documents/2008/Sort 2008/2620722395_bd5a026974_o.jpg', 
# u'Documents/2009/Sort 2009/2620722395_bd5a026974_o_d.jpg', 
# u'photos/sd600-20080702/IMG_7798.JPG', 
# u'Pictures/sd600-20080702/IMG_7798.JPG']

# Find the most common file extensions

import os
extensions = [os.path.splitext(x.filename)[1].lower() for x in ContentInstance.objects.all()]
from collections import Counter #http://stackoverflow.com/a/4746891
counter=Counter(extensions)
counter.most_common(4)
# [(u'.jpg', 277249), (u'.pdf', 15574), (u'.txt', 12857), ('', 12148)]

# -*- coding: utf-8 -*-

import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "exo.settings")
django.setup()

from exo.models import ContentKey, ContentInstance, ContentContainer, ContentSignature, Tag2
from django.db.models import Count

keys = ContentKey.objects.filter(contentsignature__picture__isnull=False).annotate(signatures=Count('contentsignature')).filter(signatures=1)
key=keys.first()
key

key.canonical = key.contentsignature_set.first()
key.save()
# Hangs... why?
# Some dumb lock

# All ContentSignatures that are the only ones pointing to their 
# ContentKey and are also Pictures should be given a resiliency
# value of 2 (Sentimental) and made the canonical object for that key

ContentKey.objects.first().contentsignature_set.count()
#1

ContentKey.objects.annotate(signatures=Count('contentsignature')).exclude(signatures=1)
#[]

ContentKey.objects.filter(contentsignature__picture__isnull=False).annotate(signatures=Count('contentsignature')).filter(signatures=1).count()
keys.first().contentsignature_set.first()

for key in keys:
    print(key.id,key.key)
    key.canonical = key.contentsignature_set.first()
    key.save()

key=keys.first()
key

key.canonical = key.contentsignature_set.first()
key.save()


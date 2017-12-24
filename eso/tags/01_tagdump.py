# -*- coding: utf-8 -*-

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "exo.settings")
import django
django.setup()

from exo.models import ContentInstance, ContentContainer, ContentSignature, ContentKey, Picture, Tag2


for tag in Tag2.objects.filter(slug='playadelfuego'):
    print(tag.slug)
    for sig in tag.contentsignature_set.all():
        print(sig.content_key.key, " ".join([t.slug for t in sig.tags.order_by('slug')]))

from django.db import connection; connection.close()

# This works much faster than I expected it to!

from django.db.models import Count
tags=Tag2.objects.annotate(tagged_sig=Count('contentsignature')).order_by('-tagged_sig')
[(t.slug, t.tagged_sig) for t in tags][0:9]

# [(u'playadelfuego', 5693), (u'thailand', 2624), (u'2013', 1326), (u'alaska', 1322), (u'newjersey', 1024), (u'2008', 927), (u'wedding', 919), (u'2002', 918), (u'16mile', 593)]

# How many untagged pictures are left
ContentSignature.objects.annotate(tags_count=Count('tags')).filter(tags_count=0).count()
# First off the stack
ContentSignature.objects.annotate(tags_count=Count('tags')).filter(tags_count=0).first().content_key.key




ContentInstance.objects.first().relpath
ContentInstance.objects.filter(relpath='JWC/Slides D All')
ContentSignature.objects.filter(contentinstance__relpath='JWC/Slides D All')


tl=Tag2.objects.filter(contentsignature__contentinstance__relpath='JWC/Slides D All').annotate(tagged_sig=Count('contentsignature')).order_by('-tagged_sig')
[(t.slug, t.tagged_sig) for t in tl]

from exo.models import Tag2

def tagrelpath(tag,relpath):
    t,created=Tag2.objects.get_or_create(slug=tag)
    for sig in ContentSignature.objects.filter(contentinstance__relpath=relpath):
        sig.tags.add(t)
        
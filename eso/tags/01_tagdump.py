# -*- coding: utf-8 -*-

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "exo.settings")
import django
django.setup()

from exo.models import ContentInstance, ContentContainer, ContentSignature, ContentKey, Picture


for tag in Tag2.objects.filter(slug='playadelfuego'):
    print tag.slug
    for sig in tag.contentsignature_set.all():
        print sig.content_key.key, " ".join([t.slug for t in sig.tags.order_by('slug')])

from django.db import connection; connection.close()

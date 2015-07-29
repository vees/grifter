# -*- coding: utf-8 -*-
"""
Created on Wed Jul 29 09:29:31 2015

@author: rob
"""

import os
import django

from exo.models import ContentInstance, ContentContainer, ContentSignature

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "exo.settings")
django.setup()

from django.db.models import Count
signatures=ContentSignature.objects.annotate(
    content_instance_count=Count('contentinstance')).filter(content_instance_count=0)

signatures = ContentSignature.objects.select_related(
    'content_key').prefetch_related('contentinstance_set').prefetch_related('contentinstance_set__content_container').annotate(
    content_instance_count=Count(
    'contentinstance')).order_by('content_instance_count')

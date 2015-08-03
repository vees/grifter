# -*- coding: utf-8 -*-
"""
Created on Sun Aug  2 20:57:04 2015

@author: rob

Also see file: docs/aws-tinkering.txt

http://boto3.readthedocs.org/en/latest/reference/services/s3.html#objectsummary
http://boto3.readthedocs.org/en/latest/guide/migrations3.html#iteration-of-buckets-and-keys
https://boto3.readthedocs.org/en/latest/guide/quickstart.html
"""

import boto3
s3 = boto3.resource('s3')

from boto3.session import Session

import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "exo.settings")
django.setup()

#TODO: Link to Django settings or some other secure location

session = Session(aws_access_key_id='', aws_secret_access_key='')
                  
s3 = session.resource('s3')
for bucket in s3.buckets.all():
    print (bucket.name)

bucket = s3.Bucket('201302-JWC')
for key in bucket.objects.all():
    print (key)
    
'''
Some discussion on the question: is ETag always MD5, and vice versa?
http://stackoverflow.com/questions/6591047/etag-definition-changed-in-amazon-s3
'''

object = s3.Object(bucket_name='201302-JWC', key='Slides AH All/Scan-130902-0018.jpg')
object.e_tag
#'"b46f2bddfdfea90879f3dd4ef7dd2674"'

from exo.models import ContentInstance, ContentContainer, ContentSignature, ContentKey, Picture

ContentInstance.objects.filter(filename__endswith='Scan-130902-0018.jpg').first().content_signature.md5
#u'b46f2bddfdfea90879f3dd4ef7dd2674'

bucket = s3.Bucket('201302-JWC')
etags = [(object.key, object.e_tag) for object in bucket.objects.all()]

etags[1000]
#('Slides AH All/Scan-130902-0019.jpg', '"b27e4b77af19a7fd3a582ac7beb8911c"')
ContentSignature.objects.filter(md5="b27e4b77af19a7fd3a582ac7beb8911c").first().contentinstance_set.first()
# <ContentInstance: 57806|Scan-130902-0019.jpg|JWC/Slides AH All|57059>



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
from django.conf import settings


session = Session(aws_access_key_id=settings.NARTHEX_AWS_ACCESS_KEY_ID,
                  aws_secret_access_key=settings.NARTHEX_AWS_ACCESS_KEY_SECRET)
                  
s3 = session.resource('s3')
for bucket in s3.buckets.all():
    print((bucket.name))

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

etags = [object.size for object in bucket.objects.all()]

etags[1000]
#('Slides AH All/Scan-130902-0019.jpg', '"b27e4b77af19a7fd3a582ac7beb8911c"')
ContentSignature.objects.filter(md5="b27e4b77af19a7fd3a582ac7beb8911c").first().contentinstance_set.first()
# <ContentInstance: 57806|Scan-130902-0019.jpg|JWC/Slides AH All|57059>


object = s3.Object(bucket_name='201302-JWC', key='Slides AH All/Scan-130902-0018.jpg')

#>>> object.__dict__
#{'bucket_name': '201302-JWC', 'meta': ResourceMeta('s3', identifiers=[u'bucket_name', u'key']), 'key': 'Slides AH All/Scan-130902-0018.jpg'}
#>>> object.content_length
#4210181
#>>> object.content_language
#>>> object.missing_meta
#>>> object.content_encoding
#>>> object.metadata
#{}
#>>> object.e_tag
#'"b46f2bddfdfea90879f3dd4ef7dd2674"'
#>>> object.expires
#>>> object.version_id
#>>> object.last_modified
#datetime.datetime(2013, 9, 9, 10, 44, 17, tzinfo=tzutc())
#>>> object.content_type
#'image/jpeg'
#>>> 

import os
bucketname='201303-CaitlinMemories'
n=0
c, created = ContentContainer.objects.get_or_create(
    server="s3.amazonaws.com", drive=bucketname, path='/')
bucket = s3.Bucket(bucketname)
for key in bucket.objects.all():
    (relpath,filename)=os.path.split(key.key)
    n+=1
    if (n % 1000 == 0):
        print(n)
    cs, createds = ContentSignature.objects.get_or_create(
        md5=key.e_tag.replace('"',""),
        content_size=key.size)
    ci, createdi = ContentInstance.objects.get_or_create(
        filename = filename,
        content_container = c,
        relpath=relpath,
        content_signature=cs)
    print("Sig",createds,"Instance", createdi,key.key)

#Sig True Instance True 01860794.ROL/60794_03.SFW
#Sig True Instance True 01860794.ROL/60794_04.SFW
#Sig True Instance True 01860794.ROL/60794_05.SFW
#Sig True Instance True 01860794.ROL/60794_06.SFW
#Sig True Instance True 01860794.ROL/60794_07.SFW
#Sig True Instance True 01860794.ROL/60794_08.SFW
#Sig True Instance True 01860794.ROL/60794_09.SFW
#Sig True Instance True 01860794.ROL/60794_10.SFW
#Sig True Instance True 01860794.ROL/60794_11.SFW
#Sig True Instance True 01860794.ROL/60794_12.SFW
#Sig True Instance True 01860794.ROL/60794_13.SFW
#Sig True Instance True 01860794.ROL/60794_14.SFW
#Sig True Instance True 01860794.ROL/60794_15.SFW
#Sig True Instance True 01860794.ROL/60794_16.SFW
#Sig True Instance True 01860794.ROL/60794_17.SFW

ContentSignature.objects.filter(md5__startswith='"').delete()

# -*- coding: utf-8 -*-

import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "exo.settings")
django.setup()

#TODO: Link to Django settings or some other secure location
from django.conf import settings

import boto3

s3 = boto3.resource('s3',
                    aws_access_key_id=settings.NARTHEX_DO_ACCESS_KEY_ID,
                    aws_secret_access_key=settings.NARTHEX_DO_ACCESS_KEY_SECRET)
                    endpoint_url='http://objects.dreamhost.com')

for bucket in s3.buckets.all():
    print (bucket.name)
    for obj in bucket.objects.all():
        print obj.key

#bucket = s3.Bucket('20150701-test')
#bucket.objects.all()
#
#etags = [(object.key, object.e_tag) for object in bucket.objects.all()]
#for key in bucket.objects.all():
#    print (key.key)
#bucket.objects.all()
#
#bucket.objects.all()[1]

import boto
import boto.s3.connection
access_key = 'put your access key here!'
secret_key = 'put your secret key here!'

conn = boto.connect_s3(
        aws_access_key_id=settings.NARTHEX_DO_ACCESS_KEY_ID,
        aws_secret_access_key=settings.NARTHEX_DO_ACCESS_KEY_SECRET)
        host = 'objects.dreamhost.com',
        calling_format = boto.s3.connection.OrdinaryCallingFormat(),
        )
        
for bucket in conn.get_all_buckets():
    print "{name}\t{created}".format(
        name = bucket.name,
        created = bucket.creation_date,
        )

i=0
for key in bucket.list():
    print "{name}\t{size}\t{modified}\t{etag}".format(
        name = key.name,
        size = key.size,
        modified = key.last_modified,
        etag = key.etag,
        )
    i+=1
    if i>5:
        break
    
list = bucket.list()

    
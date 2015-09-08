# -*- coding: utf-8 -*-

# First walk the backup directory on the local machine
# Get the filename, timestamp and the size of the file
# These are all attributes that we can also get from the S3 with boto

import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "exo.settings")
django.setup()

#TODO: Link to Django settings or some other secure location
from django.conf import settings

import os
from eso.imports import walk

path="/Volumes/dreamhost-rsync/"

#--or--
# 43 minutes 43 seconds for 50347 records
from datetime import datetime
start = datetime.now()
walked = walk.file_dir_stat_size(test_path)
end = datetime.now()
duration = end-start
print duration
#--or--
#import pickle
#walked = pickle.load( open( "/home/rob/Dropbox/NarthexDatabases/veesprod-walked.p", "rb" ) )
#--or--

import pickle
pickle.dump(walked, open("walked.p", 'wb'))


import boto3

s3 = boto3.resource('s3',
                    aws_access_key_id=settings.NARTHEX_DO_ACCESS_KEY_ID,
                    aws_secret_access_key=settings.NARTHEX_DO_ACCESS_KEY_SECRET)
                    endpoint_url='http://objects.dreamhost.com')

for bucket in s3.buckets.all():
    print (bucket.name)
    for obj in bucket.objects.all():
        print obj.key

bucket = s3.Bucket('20150701-test')
bucket.objects.all()

s3.Bucket('20150701-test').put_object(Key='test.jpg',Body='abcde')

etags = [(object.key, object.e_tag) for object in bucket.objects.all()]
for key in bucket.objects.all():
    print (key.key)
bucket.objects.all()

bucket.objects.all()[1]
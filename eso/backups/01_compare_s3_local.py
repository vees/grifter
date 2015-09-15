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

import pickle
meta2 = pickle.load( open( "/home/rob/Dropbox/NarthexDatabases/walked-dhd.p", "rb" ) )
hanjin = pickle.load( open( "/home/rob/Dropbox/NarthexDatabases/keyhash.p", "rb" ) )

hanjin1 = set([x.replace('dreamhost-rsync.sparsebundle','') for x in hanjin.keys() if x.startswith('dreamhost-rsync.sparsebundle/')])
hanjin2 = set([x.replace('dreamhost-rsync-2.sparsebundle','') for x in hanjin.keys() if x.startswith('dreamhost-rsync-2.sparsebundle/')])

hanjin1-hanjin2
hanjin2-hanjin1

metafo = set([x[0].replace('/Volumes/Meta2/dreamhost-rsync.sparsebundle','') for x in meta2])

metafo-hanjin2
hanjin2-metafo

hanjin3 = {x.replace('dreamhost-rsync-2.sparsebundle',''): hanjin[x][2].replace('"','') for x in hanjin.keys() if x.startswith('dreamhost-rsync-2.sparsebundle/')}

hanjin.keys()[0]
hanjin['dreamhost-rsync-2.sparsebundle/bands/b03']

meta3 = {x[0].replace('/Volumes/Meta2/dreamhost-rsync.sparsebundle',''): x[6] for x in meta2}

for name,md5 in meta3.iteritems():
    if (hanjin3[name] != md5):
        print name,md5 
    
#/bands/e0 246cf878a052700a9257d553412bcc1a
#/bands/75 f8ed2fb8af768fc4fd205d701ad90b6a
#/bands/76 2a3bd3bb50f5017edf075ef429ce261d
#/bands/78 37ccaaa70ab19a3eb611b8e07a8dd029
#/bands/79 c73dbeaae97795bfacbd204f4314ff54
#/bands/11d9 d0b7126fe69712e5ef23b261af9d791c
#/bands/c b81d20d62499f87f7347b0ba993fb68e
#/bands/0 0845c9b2952918c8319a611935247e49

set(meta3.keys())-set(hanjin3.keys())

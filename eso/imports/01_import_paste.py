# -*- coding: utf-8 -*-
"""
Created on Sat Jul  4 17:48:13 2015
@author: rob
"""

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "exo.settings")
import django
django.setup()

from exo.models import ContentInstance, ContentContainer, ContentSignature

test_path = "/home/veesprod/vees.net/photos"


# Working with a content container creation
# Using a handy function from here:
# https://docs.djangoproject.com/en/dev/ref/models/querysets/#get-or-create
# http://stackoverflow.com/questions/8766222/django-create-if-doesnt-exist

from eso.imports import walk

#--or--
# 43 minutes 43 seconds for 50347 records
from datetime import datetime
start = datetime.now()
walked = walk.file_dir_stat_size(test_path)
end = datetime.now()
duration = end-start
print(duration)
#--or--
import pickle
walked = pickle.load( open( "/home/rob/Dropbox/NarthexDatabases/"
    "veesprod-walked.p", "rb" ) )
#--or--

import pickle
pickle.dump(walked, open("walked-dhd.p", 'wb'))

walked[766][7]
walkunit=walked[766]

'''
Here's a walkthrough of arbritary content into the
data structure.
Even on MySQL a 50k row import takes over two hours
'''
n=0
c, created = ContentContainer.objects.get_or_create(
    server="skymaster", drive="veesprod", path=test_path)
for walkunit in walked:
    n+=1
    if (n % 1000 == 0):
        print(n)
    cs, createds = ContentSignature.objects.get_or_create(
        md5=walkunit[6], sha2=walkunit[7],
        content_size=walkunit[5])
    ci, createdi = ContentInstance.objects.get_or_create(
        filename = walkunit[2],
        content_container = c,
        relpath=walkunit[3],
        stat_hash=walkunit[4],
        content_signature=cs)
    print("Sig",createds,"Instance", createdi,walkunit[2])


#https://docs.djangoproject.com/en/dev/topics/db/queries/#following-relationships-backward
ContentSignature.objects.all()[1].contentinstance_set.all()
ContentSignature.objects.filter(n_contentinstance__gt=1)

#http://stackoverflow.com/a/6525869
from django.db.models import Count
ContentSignature.objects.annotate(instance_count=Count('contentinstance')).filter(instance_count__gt=1).count()

for hashitem in ContentSignature.objects.annotate(instance_count=Count('contentinstance')).filter(instance_count__gt=1).exclude(content_key=None):
    print(hashitem.content_key.key,hashitem.md5,hashitem.sha2,hashitem.content_size)
    for location in hashitem.contentinstance_set.all():
        print(location.content_container.server,location.content_container.drive,location.content_container.path,location.relpath,location.filename)
    print()

#Not exactly what I anticipated, so lets reload
ContentInstance.objects.all().delete()

import sys
sys.exit()

#walked = walk.files_and_stat(walk.files_under_dir(test_path))
#len(walked)

walkedfile = walked[66]

# ('/Users/rob/Desktop/Inbox/10556513_1494047140880868_372632801882824292_n.jpg', 7224436048908003272, 61877)

os.path.relpath(walked[7][0],test_path)

from eso.imports import load_masterfile

# Duration of less than a second for ~6000 files
from datetime import datetime
start = datetime.now()
foo = walk.files_and_stat(walk.files_under_dir(test_path))
end = datetime.now()
duration = end-start
print(duration)

start = datetime.now()
foo = walk.files_and_stat(walk.files_under_dir(test_path))
end = datetime.now()
duration = end-start
print(duration)

[load_masterfile.hash_parse(file[0]) for file in walk]

# Here's a fun spot where I loaded the same key twice and tried to delete it

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "exo.settings")
import django
django.setup()
from exo.models import ContentInstance, ContentContainer, ContentSignature, ContentKey
ContentContainer.objects.all()
#ContentContainer.objects.all()[1].delete()


def get_hostname():
    import socket
    return socket.gethostname()

get_hostname()

ContentSignature.objects.all()
from eso.imports import randspace
randspace.randid()

for sig in ContentSignature.objects.all():
    sig.content_key=None
    sig.save()

# Give everything a content key (accession number)

from exo.models import ContentInstance, ContentContainer, ContentSignature, ContentKey
import eso.base32.randspace
cs = ContentSignature.objects.filter(content_key=None)
for sig in cs:
    try:
        duplicate_key=1
        while duplicate_key>0:
            newkey=eso.base32.randspace.randid()
            duplicate_key=ContentKey.objects.filter(key=newkey).count()
        ck = ContentKey.objects.create(key=newkey)
        sig.content_key=ck
        sig.save()
    except django.db.utils.IntegrityError:
        print("duplicate key %s for sig id %s" % (newkey, cs.id))
        continue

# Blow away content keys
#
#import os
#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "exo.settings")
#import django
#django.setup()
#from exo.models import ContentInstance, ContentContainer, ContentSignature, ContentKey
#ContentKey.objects.all().delete()


zerothfile=ContentKey.objects.filter(key='pf6d').first().contentsignature_set.all().first().contentinstance_set.all().first()
"/".join([zerothfile.content_container.path,zerothfile.relpath,zerothfile.filename])

ContentSignature.objects.all()


from django.core import serializers
foo = serializers.serialize('json', list(ContentSignature.objects.all()) + list(ContentInstance.objects.all()) + list(ContentKey.objects.all()))

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "exo.settings")
import django
django.setup()

from exo.models import ContentInstance, ContentContainer, ContentSignature, ContentKey
ContentInstance.objects.all()

from exo.models import PictureSimple
PictureSimple.objects.all()

# Abbreviated version for updates

from eso.imports import walk
test_path='/home/veesprod/vees.net/photos/iPhone-20150621'
walked = walk.file_dir_stat_size(test_path)

#>>> walked[0]
#('/home/veesprod/vees.net/photos/rickettsglen15/IMG_2211.JPG', '/home/veesprod/vees.net/photos/rickettsglen15', 'IMG_2211.JPG', '.', 140071267384044659, 7431398, 'd7be8bb8cbd0342a0fed1765e47d8edb', '21712f2df91a39da7601cfdf4aff1780ed00a7f23a6801c1b1d84966d107205e')

# Just need to either change walkunit[3] to rickettsglen15 in situ
# or modify the import function accordingly. Method 1 seems easier,
# except that they are tuples so the following doesn't work

#for walkunit in walked:
#    walkunit[3] = 'iPhone-20150621'

# TypeError: 'tuple' object does not support item assignment

# So instead lets copy the whole function over

from exo.models import ContentInstance, ContentContainer, ContentSignature

n=0
c, created = ContentContainer.objects.get_or_create(
    server="skymaster", drive="veesprod", path='/home/veesprod/vees.net/photos')
for walkunit in walked:
    n+=1
    if (n % 1000 == 0):
        print(n)
    cs, createds = ContentSignature.objects.get_or_create(
        md5=walkunit[6], sha2=walkunit[7],
        content_size=walkunit[5])
    ci, createdi = ContentInstance.objects.get_or_create(
        filename = walkunit[2],
        content_container = c,
        relpath='iPhone-20150621',
        stat_hash=walkunit[4],
        content_signature=cs)
    print("Sig",createds,"Instance", createdi,walkunit[2])

# ...100 records...
# Sig True Instance True IMG_2386.JPG

#>>> ContentInstance.objects.filter(relpath='rickettsglen15').count()
#218
#>>> ContentSignature.objects.filter(content_key=None).count()
#218

#So we are safe to do the following:
# Give everything a content key (accession number)

#>>> from exo.models import Tag2
#>>>
#>>> def tagrelpath(tag,relpath):
#...     t,created=Tag2.objects.get_or_create(slug=tag)
#...     for sig in ContentSignature.objects.filter(contentinstance__relpath=relpath):
#...         sig.tags.add(t)
#...
#>>> tagrelpath('rickettsglen','rickettsglen15')
#>>> tagrelpath('pennsylvania','rickettsglen15')
#>>> tagrelpath('by:cindycarlson','rickettsglen15')
#>>> tagrelpath('2015','rickettsglen15')

#TODO: Automate the above

# -*- coding: utf-8 -*-
"""
Created on Sat Jul  4 17:48:13 2015

@author: rob
"""

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "exo.settings")
import django
django.setup()

from exo.models import *

test_path = "/Users/rob/Desktop"

# Working with a content container creation
# Using a handy function from here:
# https://docs.djangoproject.com/en/dev/ref/models/querysets/#get-or-create
# http://stackoverflow.com/questions/8766222/django-create-if-doesnt-exist

c, created = ContentContainer.objects.get_or_create(
    server="love", drive="love", path=test_path)

from eso.imports import walk

walked = walk.files_and_stat(walk.files_under_dir(test_path))
len(walked)

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
print duration

start = datetime.now()
foo = walk.files_and_stat(walk.files_under_dir(test_path))
end = datetime.now()
duration = end-start
print duration

[load_masterfile.hash_parse(file[0]) for file in walk]

# Here's a fun spot where I loaded the same key twice and tried to delete it

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "exo.settings")
import django
django.setup()
from exo.models import *
ContentContainer.objects.all()
#ContentContainer.objects.all()[1].delete()


def get_hostname():
    import socket
    return socket.gethostname()

get_hostname()

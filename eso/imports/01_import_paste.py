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

c=ContentContainer()
c.server = "love"
c.drive = "love"
c.path = "/Users/rob/Desktop"
c.save()

from eso.imports import walk

walk = walk.files_and_stat(walk.files_under_dir(test_path))

len(walk)

from eso.imports import load_masterfile
[load_masterfile.hash_parse(file[0]) for file in walk]

# Duration of less than a second for ~6000 files
from datetime import datetime
start = datetime.now()
foo = walk.files_and_stat(walk.files_under_dir(test_path))
end = datetime.now()
duration = end-start
print duration


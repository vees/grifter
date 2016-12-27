# -*- coding: utf-8 -*-
"""
Created on Wed Aug 12 13:54:20 2015

@author: rob
"""

from PIL import Image
import StringIO


im=Image.open('/media/dev/photos/pdfpan-08s/Playa_del_Fuego_Spring_2008_Panorama_Cloned.jpg')
im.size
#(26813, 2141)

im=im.rotate(90)
size = 1024,1024
im.thumbnail(size, Image.ANTIALIAS)
buf= StringIO.StringIO()
im.save(buf, format= 'JPEG')

im.size

import hashlib

content=buf.getvalue()

md5hash = hashlib.md5(content).hexdigest()
sha2hash = hashlib.sha256(content).hexdigest()

md5hash,sha2hash

# ('5f714532cc89689ff5b887c976af85b7333b9af58b5c0186d35a12c2e18303a0', '60ba4e6d10e8dcd70955a8ba746a2c76')
f=open("/home/rob/test.jpg", "w")
im.save(f, format='JPEG')
f.close()

#rob@wrath:~$ md5sum test.jpg
#60ba4e6d10e8dcd70955a8ba746a2c76  test.jpg


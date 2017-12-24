# -*- coding: utf-8 -*-
"""
Created on Wed Aug 12 13:54:20 2015

@author: rob
"""

from PIL import Image
import io

import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "exo.settings")
django.setup()

from exo.models import ContentKey, ContentInstance, ContentContainer, ContentSignature, Tag2
from django.db.models import Count

instance=ContentInstance.objects.filter(content_container__id=2).filter(filename__endswith='.jpg').first()
filename="/".join([instance.content_container.path,instance.relpath,instance.filename])
# u'/Users/rob/Desktop/Duplicates/2012-09-24_21-43-25_816.jpg'
im=Image.open(filename)
im.size
# (2048, 1536)

from django.conf import settings

w=1024
h=1024
r=270

if r!=0:
    im=im.rotate(r)
size = (w,h)
im.thumbnail(size, Image.ANTIALIAS)
buf= io.StringIO()
im.save(buf, format= 'JPEG')
content=buf.getvalue()

import hashlib

md5hash = hashlib.md5(content).hexdigest()
sha2hash = hashlib.sha256(content).hexdigest()
size = len(content)

newsig = ContentSignature.objects.create(
    md5 = md5hash, 
    sha2 = sha2hash,
    content_size = size,
    content_key = instance.content_signature.content_key,
    resiliency = 1,
    derived_from = instance.content_signature)

#class TransformedPicture(models.Model):
#    signature = models.OneToOneField(ContentSignature, primary_key=True)
#    request_width = models.IntegerField(null=True)
#    request_height = models.IntegerField(null=True)
#    request_rotation = models.IntegerField(null=True)
#    result_width = models.IntegerField(null=True)
#    result_height = models.IntegerField(null=True)
#    result_rotation = models.IntegerField(null=True)

'''Update this model to contain a combined key for the six factors'''

from exo.models import TransformedPicture

transform = TransformedPicture.objects.create(
    signature = newsig,
    request_width = w,
    request_height = h,
    request_rotation = r,
    result_width = im.size[0],
    result_height = im.size[1],
    result_rotation = r,
)

#filename = models.CharField(max_length=200)
#content_container = models.ForeignKey(ContentContainer, null=False)
#relpath = models.CharField(max_length=200)
#stat_hash = models.BigIntegerField(null=True)
#first_seen = models.DateTimeField(null=True)
#verified_on = models.DateTimeField(null=True)
#content_signature = models.ForeignKey(ContentSignature, null=True)

container = ContentContainer.objects.filter(id=settings.NARTHEX_CONTAINER_ID).first()
container.path

newinstance = ContentInstance.objects.create(
    filename=sha2hash+'.jpg',
    content_container = container,
    relpath = 'resizedcache',
    content_signature = newsig,
)

cachedir="/".join([container.path,'resizedcache'])
newfilename="/".join([cachedir,sha2hash+'.jpg'])
import os
if not os.path.exists(cachedir):
    os.makedirs(cachedir)
# u'/Users/rob/Desktop/resizedcache/86d51ad4d427b45d2966d23e1af95627165e87c611355d090024fcf1f015b8a8.jpg'

f=open(newfilename, "w")
im.save(f, format='JPEG')
f.close()

ContentKey.objects.filter(key='cy1h').last().contentsignature_set.all()
#[<ContentSignature: 50337|89a042bf9d14d3b0155f93a14480343b|96166e00d046b20c8de587a721a4f668d8c48262dd6048e8b500fd176e4d8e04|1084780>,
# <ContentSignature: 182245|4a021950fe5f487f47e511b2d35a84a0|86d51ad4d427b45d2966d23e1af95627165e87c611355d090024fcf1f015b8a8|85777>, 
# <ContentSignature: 182246|4a021950fe5f487f47e511b2d35a84a0|86d51ad4d427b45d2966d23e1af95627165e87c611355d090024fcf1f015b8a8|85777>, 
# <ContentSignature: 182247|f4f88779283afa745b7b2808d9f08ada|f0f23a5004db93da17b8e7e814ea9ef8d113cb8320d2d6a64a9caa50ae9cb7a6|85938>, 
# <ContentSignature: 182248|8fcd20716965220150e4af65075b9011|586044ebc8e7c75ae0e7fe45b18c79432b069f02f1b2547424c326e272aff81c|85925>]

ContentKey.objects.filter(key='cy1h').last().contentsignature_set.last().transformedpicture.__dict__
#{'result_height': 1024L, 'result_width': 768L, 'request_rotation': 270L, 'signature_id': 182248L, 'result_rotation': 270L, 'request_height': 1024L, 'request_width': 1024L}

ContentSignature.objects.filter(resiliency=1).count()
# 4

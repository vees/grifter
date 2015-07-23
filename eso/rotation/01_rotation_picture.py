# -*- coding: utf-8 -*-

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "exo.settings")
import django
django.setup()

from django.conf import settings

from exo.models import ContentInstance, ContentContainer, ContentSignature, ContentKey, Picture, Tag2

contentkey='hy4r'
contentkey='ds1z'
ContentKey.objects.filter(key=contentkey).first().contentsignature_set.all().first().picture.rotation
cs=ContentKey.objects.filter(key=contentkey).first().contentsignature_set.all().first()


# What does this look like
Picture.objects.first().__dict__
hasattr(cs, 'picture')

from django.db import connection; connection.close()

def addrotation(key, rotation):
    sig=ContentKey.objects.filter(key=key).first().contentsignature_set.all().first()
    p,new=Picture.objects.update_or_create(signature=sig, defaults={'rotation': rotation})
    return sig,p.rotation,new
    
def addrating(key, rating):
    sig=ContentKey.objects.filter(key=key).first().contentsignature_set.all().first()
    p,new=Picture.objects.update_or_create(signature=sig, defaults={'rating': rating})
    return sig,p.rotation,new

def addtag(key, tag):
    t,created=Tag2.objects.update_or_create(slug=tag)
    sig=ContentKey.objects.filter(key=key).first().contentsignature_set.all().first()
    sig.tags.add(t)
    
#p,new=Picture.objects.update_or_create(signature=sig, defaults={'rotation': rotation})

addrotation('bm5k', 270)

Picture.objects.filter(signature__content_key__key='bn3g').first().rotation

addrotation('3xcf', 90)


# Lets talk about ratings, baby
# How did I rate things in the past?

Picture.objects.filter(rating=0).first().signature.content_key.key
# 3ppr- picture of a rash, probably means "remove" or "hide"
Picture.objects.filter(rating=1).first().signature.content_key.key
# pwt4 people walking away from me
Picture.objects.filter(rating=2).first().signature.content_key.key
#jn2q - picture of a rock and some feet
Picture.objects.filter(rating=3).first().signature.content_key.key
# ny7s flowers, low depth of field
Picture.objects.filter(rating=4).first().signature.content_key.key
# nnd1 Coral reef, bad color distribution, etc.
Picture.objects.filter(rating=5).first().signature.content_key.key
# 7rhd - Pictuesque landscape

contentkey='h7zg'
ContentKey.objects.filter(key=contentkey).first().contentsignature_set.all().first().picture.__dict__



contentkey='h7zg'
ContentKey.objects.filter(key=contentkey).first().contentsignature_set.all().first().tags.all()
Tag2.objects.all()

def tagrelpath(tag,relpath):
    t,created=Tag2.objects.get_or_create(slug=tag)
    for sig in ContentSignature.objects.filter(contentinstance__relpath=relpath):
        sig.tags.add(t)

tagrelpath('playadelfuego','pdf04f2')

# Deleting a tag from everything in a relpath when added by accident
Tag2.objects.filter(contentsignature__contentinstance__relpath='suzystaff04sep').filter(slug='2014').delete()

tagdump = dict([(t.slug, [s.md5 for s in t.contentsignature_set.all()]) for t in Tag2.objects.all().order_by('slug')])
import json
response = json.dumps(tagdump)
response[1:1000]

Tag2.objects.first().contentsignature_set.all()

Picture.objects.filter(rotation__isnull=False).count()
[(p.rotation, p.signature.sha2) for p in Picture.objects.filter(rotation__isnull=False)]
dict([(p.signature.sha2, {'rotation': p.rotation}) for p in Picture.objects.filter(rotation__isnull=False).prefetch_related()[1:1000]])


import requests
import requests
import json

vees = 'https://vees.net/'
local = 'http://127.0.0.1:8000/'

def crosssync(source,dest,endpoint):
    payload=requests.get(source+'api/%s/dumpall' % (endpoint), verify=False).text
    veestags=json.loads(payload)
    for key,itemlist in veestags.iteritems():
        print key
        r=requests.post(dest+"api/%s/load" % (endpoint), data=json.dumps({key: itemlist}), verify=False)
        print r.text

crosssync(vees,local,'tags')
crosssync(local,vees,'tags')

crosssync(vees,local,'rotation')
crosssync(local,vees,'rotation')



r=requests.post("http://127.0.0.1:8000/api/tags/load", data=payload)
print r.text
payload=requests.get('http://127.0.0.1:8000/api/tags/dumpall').text
r=requests.post("https://vees.net/api/tags/load", data=payload)
print r.text

import requests



payload=requests.get('https://vees.net/api/rotation/dumpall', verify=False).text
r=requests.post("http://127.0.0.1:8000/api/rotation/load", data=payload)
r.text

payload=requests.get('http://127.0.0.1:8000/api/rotation/dumpall').text
r=requests.post("https://vees.net/api/rotation/load", data=payload, verify=False)
r.text

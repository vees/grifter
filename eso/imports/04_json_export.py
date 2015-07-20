# -*- coding: utf-8 -*-
"""
Created on Mon Jul 20 09:45:38 2015

@author: rob
"""

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "exo.settings")
import django
django.setup()


from exo.models import ContentInstance, ContentContainer, ContentSignature, ContentKey, Picture

from django.core import serializers

all_objects = ContentInstance.objects.all()
data = serializers.serialize('json', all_objects[11:12])

data

ci=ContentInstance.objects.first()

ci._meta.fields

ci.__dict__
import json
json.dumps(ci.__dict__, sort_keys=True, indent=4)

ci=ContentInstance.objects.select_related().first()
json.dumps(ci.__dict__, sort_keys=True, indent=4)



ci=ContentInstance.objects.select_related().first()
ci.__dict__

ci=ContentInstance.objects.select_related().prefetch_related('content_signature__content_key').first()
ci.__dict__

# From http://stackoverflow.com/a/3768975/682915
class MyEncoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__
        
json.dumps(ci, cls=MyEncoder, sort_keys=True)

#Gives the following output:
'''
{
    "_content_container_cache": {
        "_state": {
            "adding": false, 
            "db": "default"
        }, 
        "drive": "309", 
        "id": 1, 
        "path": "/media/dev/photos", 
        "server": "wrath"
    }, 
    "_content_signature_cache": {
        "_content_key_cache": {
            "_state": {
                "adding": false, 
                "db": "default"
            }, 
            "id": 1, 
            "key": "t2en"
        }, 
        "_prefetched_objects_cache": {}, 
        "_state": {
            "adding": false, 
            "db": "default"
        }, 
        "content_key_id": 1, 
        "content_size": 780059, 
        "id": 1, 
        "md5": "02b217cbb82ace3880f8803cb87fde77", 
        "sha2": "4acf3a512ce56cffa94098dd9d920d36e55e306b7e44b1b656bc8a42c9487caf"
    }, 
    "_prefetched_objects_cache": {}, 
    "_state": {
        "adding": false, 
        "db": "default"
    }, 
    "content_container_id": 1, 
    "content_signature_id": 1, 
    "filename": "IMG_1965.JPG", 
    "first_seen": null, 
    "id": 1, 
    "relpath": "sd600-20090224", 
    "stat_hash": 647727110, 
    "verified_on": null
}
'''

# Lambda function for datetime to ISO format per http://stackoverflow.com/a/2680060/682915
dthandler = lambda obj: (
    obj.isoformat()
    if isinstance(obj, datetime.datetime)
    or isinstance(obj, datetime.date)
    else None)
json.dumps(datetime.datetime(2011, 3, 16, 21, 59, 32), default=dthandler)



json.loads('''{
    "content_container": {
        "drive": "309", 
        "path": "/media/dev/photos", 
        "server": "wrath"
    }, 
    "content_signature": {
        "content_key": {
            "key": "t2en"
        }, 
        "content_size": 780059, 
        "md5": "02b217cbb82ace3880f8803cb87fde77", 
        "sha2": "4acf3a512ce56cffa94098dd9d920d36e55e306b7e44b1b656bc8a42c9487caf",
        "picture": {
            "rating": 6,
            "taken_on": "2011-03-16T21:59:32",
            "height": 1704,
            "width": 2272,
            "rotation": 0
        }
    },
    "filename": "IMG_1965.JPG", 
    "first_seen": null, 
    "relpath": "sd600-20090224", 
    "stat_hash": 647727110, 
    "verified_on": null
}''')

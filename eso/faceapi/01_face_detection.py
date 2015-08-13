# -*- coding: utf-8 -*-
"""
Created on Thu Aug 13 13:54:32 2015

@author: rob
"""

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "exo.settings")
import django
django.setup()

from exo.models import ContentInstance, ContentContainer, ContentSignature

# Fetch all pictures with the tag jwcjr 
# chn4

# Retrieve the first contentsignature with the contentinstance

# If a rotation exists, IM rotate

# Send image to FACE API

# https://api.projectoxford.ai/face/v0/detections[?analyzesFaceLandmarks][&analyzesAge][&analyzesGender][&analyzesHeadPose]

instance=ContentSignature.objects.filter(md5='eebb8f2546b5c1f8a0caecf6cbcbf442').first().contentinstance_set.first()
filename = instance.content_container.path + '/' + instance.relpath + '/' + instance.filename

# Using sample from http://4ve.es/AlI

import urllib
import httplib
from django.conf import settings

params = urllib.urlencode({
    'subscription-key': settings.NARTHEX_FACEAPI_PRIMARYKEY,
    'analyzesFaceLandmarks': 'true',
    'analyzesAge': 'true',
    'analyzesGender': 'true',
    'analyzesHeadPose': 'true',
}) 

#specify image from file
#For a local image, Content-Type should be application/octet-stream or multipart/form-data AND JSON SHOULD BE EMPTY

headers = {
    'Content-type': 'application/octet-stream',
}

body = "" 

#load image
f = open(filename, "rb")
body = f.read()
f.close()

conn = httplib.HTTPSConnection('api.projectoxford.ai')
conn.request("POST", "/face/v0/detections?%s" % params, body, headers)
response = conn.getresponse("")
data = response.read()
print(data)
conn.close()

# [{"faceId":"23053d75-2a32-4c33-a43b-fd98c7bfeb40","faceRectangle":{"top":585,"left":850,"width":459,"height":459},"faceLandmarks":{"pupilLeft":{"x":980.6,"y":708.8},"pupilRight":{"x":1180.2,"y":703.0},"noseTip":{"x":1056.3,"y":832.4},"mouthLeft":{"x":1003.4,"y":928.5},"mouthRight":{"x":1174.4,"y":920.8},"eyebrowLeftOuter":{"x":894.6,"y":681.7},"eyebrowLeftInner":{"x":1023.2,"y":690.5},"eyeLeftOuter":{"x":947.5,"y":713.6},"eyeLeftTop":{"x":980.1,"y":696.2},"eyeLeftBottom":{"x":980.6,"y":721.2},"eyeLeftInner":{"x":1013.0,"y":708.8},"eyebrowRightInner":{"x":1113.9,"y":679.4},"eyebrowRightOuter":{"x":1255.1,"y":689.1},"eyeRightInner":{"x":1145.8,"y":703.3},"eyeRightTop":{"x":1178.9,"y":690.8},"eyeRightBottom":{"x":1179.0,"y":712.7},"eyeRightOuter":{"x":1210.8,"y":709.2},"noseRootLeft":{"x":1036.8,"y":714.2},"noseRootRight":{"x":1092.2,"y":711.8},"noseLeftAlarTop":{"x":1021.2,"y":796.1},"noseRightAlarTop":{"x":1110.7,"y":789.8},"noseLeftAlarOutTip":{"x":1002.0,"y":834.8},"noseRightAlarOutTip":{"x":1143.8,"y":828.9},"upperLipTop":{"x":1079.9,"y":904.2},"upperLipBottom":{"x":1080.3,"y":924.9},"underLipTop":{"x":1083.0,"y":940.8},"underLipBottom":{"x":1086.6,"y":955.5}},"attributes":{"headPose":{"pitch":0.0,"roll":-1.4,"yaw":-12.9},"gender":"male","age":77}}]

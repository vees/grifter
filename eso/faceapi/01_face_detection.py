# -*- coding: utf-8 -*-
"""
Created on Thu Aug 13 13:54:32 2015

@author: rob
"""

import urllib.request, urllib.parse, urllib.error
import http.client
from django.conf import settings

from exo.models import ContentSignature

def callFaceApi(filecontent):
    # Using sample from http://4ve.es/AlI
    params = urllib.parse.urlencode({
        'subscription-key': settings.NARTHEX_FACEAPI_PRIMARYKEY,
        'analyzesFaceLandmarks': 'true',
        'analyzesAge': 'true',
        'analyzesGender': 'true',
        'analyzesHeadPose': 'true',
    }) 
    #For a local image, Content-Type should be application/octet-stream or multipart/form-data AND JSON SHOULD BE EMPTY
    headers = {
        'Content-type': 'application/octet-stream',
    }
    conn = http.client.HTTPSConnection('api.projectoxford.ai')
    conn.request("POST", "/face/v0/detections?%s" % params, filecontent, headers)
    response = conn.getresponse("")
    data = response.read()
    conn.close()
    return data

def getFilenameByKey(key):
    signature = ContentSignature.objects.filter(content_key__key=key).first()
    instance = signature.contentinstance_set.first()
    filename = instance.content_container.path + '/' + instance.relpath + '/' + instance.filename
    return filename

def getFaceByKey(key):
    filename = getFilenameByKey(key)    
    #load image
    f = open(filename, "rb")
    filecontent = f.read()
    # Rotate here
    f.close()
    result = callFaceApi(filecontent)
    return result

# Fetch all pictures with the tag jwcjr 
# chn4

# Retrieve the first contentsignature with the contentinstance

# If a rotation exists, IM rotate

# Send image to FACE API

# https://api.projectoxford.ai/face/v0/detections[?analyzesFaceLandmarks][&analyzesAge][&analyzesGender][&analyzesHeadPose]

# chn4
# [{"faceId":"23053d75-2a32-4c33-a43b-fd98c7bfeb40","faceRectangle":{"top":585,"left":850,"width":459,"height":459},"faceLandmarks":{"pupilLeft":{"x":980.6,"y":708.8},"pupilRight":{"x":1180.2,"y":703.0},"noseTip":{"x":1056.3,"y":832.4},"mouthLeft":{"x":1003.4,"y":928.5},"mouthRight":{"x":1174.4,"y":920.8},"eyebrowLeftOuter":{"x":894.6,"y":681.7},"eyebrowLeftInner":{"x":1023.2,"y":690.5},"eyeLeftOuter":{"x":947.5,"y":713.6},"eyeLeftTop":{"x":980.1,"y":696.2},"eyeLeftBottom":{"x":980.6,"y":721.2},"eyeLeftInner":{"x":1013.0,"y":708.8},"eyebrowRightInner":{"x":1113.9,"y":679.4},"eyebrowRightOuter":{"x":1255.1,"y":689.1},"eyeRightInner":{"x":1145.8,"y":703.3},"eyeRightTop":{"x":1178.9,"y":690.8},"eyeRightBottom":{"x":1179.0,"y":712.7},"eyeRightOuter":{"x":1210.8,"y":709.2},"noseRootLeft":{"x":1036.8,"y":714.2},"noseRootRight":{"x":1092.2,"y":711.8},"noseLeftAlarTop":{"x":1021.2,"y":796.1},"noseRightAlarTop":{"x":1110.7,"y":789.8},"noseLeftAlarOutTip":{"x":1002.0,"y":834.8},"noseRightAlarOutTip":{"x":1143.8,"y":828.9},"upperLipTop":{"x":1079.9,"y":904.2},"upperLipBottom":{"x":1080.3,"y":924.9},"underLipTop":{"x":1083.0,"y":940.8},"underLipBottom":{"x":1086.6,"y":955.5}},"attributes":{"headPose":{"pitch":0.0,"roll":-1.4,"yaw":-12.9},"gender":"male","age":77}}]

if __name__ == "__main__":
    import os
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "exo.settings")
    import django
    django.setup()

    a=getFaceByKey('by3e')

#by3e
#'[{"faceId":"b8d0b923-cf0b-4833-a136-3b2cf19cc3b5","faceRectangle":{"top":602,"left":1048,"width":147,"height":147},"faceLandmarks":{"pupilLeft":{"x":1086.7,"y":643.3},"pupilRight":{"x":1147.3,"y":638.0},"noseTip":{"x":1135.5,"y":678.5},"mouthLeft":{"x":1090.5,"y":714.6},"mouthRight":{"x":1145.1,"y":708.0},"eyebrowLeftOuter":{"x":1060.9,"y":634.5},"eyebrowLeftInner":{"x":1113.8,"y":628.3},"eyeLeftOuter":{"x":1075.9,"y":646.0},"eyeLeftTop":{"x":1087.8,"y":639.9},"eyeLeftBottom":{"x":1088.2,"y":647.7},"eyeLeftInner":{"x":1098.9,"y":643.0},"eyebrowRightInner":{"x":1135.4,"y":627.9},"eyebrowRightOuter":{"x":1165.3,"y":621.5},"eyeRightInner":{"x":1136.3,"y":639.3},"eyeRightTop":{"x":1145.7,"y":634.9},"eyeRightBottom":{"x":1146.3,"y":641.1},"eyeRightOuter":{"x":1155.1,"y":638.0},"noseRootLeft":{"x":1115.4,"y":645.5},"noseRootRight":{"x":1133.0,"y":644.2},"noseLeftAlarTop":{"x":1111.3,"y":671.3},"noseRightAlarTop":{"x":1138.9,"y":666.6},"noseLeftAlarOutTip":{"x":1104.4,"y":685.1},"noseRightAlarOutTip":{"x":1145.5,"y":679.6},"upperLipTop":{"x":1127.5,"y":703.7},"upperLipBottom":{"x":1127.7,"y":710.7},"underLipTop":{"x":1127.2,"y":712.3},"underLipBottom":{"x":1128.3,"y":718.9}},"attributes":{"headPose":{"pitch":0.0,"roll":-5.9,"yaw":29.2},"gender":"female","age":76}}]'

#r1ej
#'[{"faceId":"16ff6ff7-4634-4db2-adc3-d781a7ad6af5","faceRectangle":{"top":596,"left":963,"width":78,"height":78},"faceLandmarks":{"pupilLeft":{"x":983.2,"y":618.2},"pupilRight":{"x":1019.4,"y":617.3},"noseTip":{"x":1003.9,"y":637.9},"mouthLeft":{"x":982.7,"y":651.1},"mouthRight":{"x":1017.1,"y":650.8},"eyebrowLeftOuter":{"x":972.9,"y":614.3},"eyebrowLeftInner":{"x":998.3,"y":613.6},"eyeLeftOuter":{"x":977.0,"y":618.1},"eyeLeftTop":{"x":983.0,"y":616.7},"eyeLeftBottom":{"x":983.4,"y":619.3},"eyeLeftInner":{"x":988.7,"y":617.5},"eyebrowRightInner":{"x":1008.1,"y":613.2},"eyebrowRightOuter":{"x":1029.5,"y":614.5},"eyeRightInner":{"x":1013.4,"y":616.8},"eyeRightTop":{"x":1019.0,"y":615.5},"eyeRightBottom":{"x":1018.7,"y":618.0},"eyeRightOuter":{"x":1023.4,"y":616.7},"noseRootLeft":{"x":997.0,"y":618.5},"noseRootRight":{"x":1007.1,"y":618.4},"noseLeftAlarTop":{"x":994.7,"y":630.0},"noseRightAlarTop":{"x":1010.8,"y":629.8},"noseLeftAlarOutTip":{"x":991.2,"y":636.8},"noseRightAlarOutTip":{"x":1014.6,"y":636.2},"upperLipTop":{"x":1000.8,"y":647.2},"upperLipBottom":{"x":1000.8,"y":650.1},"underLipTop":{"x":1000.7,"y":658.8},"underLipBottom":{"x":1000.6,"y":663.3}},"attributes":{"headPose":{"pitch":0.0,"roll":0.0,"yaw":8.8},"gender":"male","age":36}},{"faceId":"2f9cf2ea-6792-4028-ba64-ed9dea4717d2","faceRectangle":{"top":619,"left":1142,"width":72,"height":72},"faceLandmarks":{"pupilLeft":{"x":1158.5,"y":642.9},"pupilRight":{"x":1192.4,"y":637.8},"noseTip":{"x":1177.7,"y":656.1},"mouthLeft":{"x":1164.8,"y":673.1},"mouthRight":{"x":1196.7,"y":668.2},"eyebrowLeftOuter":{"x":1148.3,"y":636.9},"eyebrowLeftInner":{"x":1171.1,"y":634.1},"eyeLeftOuter":{"x":1152.1,"y":642.8},"eyeLeftTop":{"x":1157.4,"y":640.7},"eyeLeftBottom":{"x":1158.2,"y":642.8},"eyeLeftInner":{"x":1163.4,"y":640.6},"eyebrowRightInner":{"x":1177.3,"y":632.2},"eyebrowRightOuter":{"x":1198.8,"y":631.5},"eyeRightInner":{"x":1185.6,"y":637.5},"eyeRightTop":{"x":1190.4,"y":635.8},"eyeRightBottom":{"x":1190.5,"y":638.6},"eyeRightOuter":{"x":1195.3,"y":636.9},"noseRootLeft":{"x":1169.9,"y":640.2},"noseRootRight":{"x":1179.1,"y":638.3},"noseLeftAlarTop":{"x":1170.9,"y":650.8},"noseRightAlarTop":{"x":1184.6,"y":649.8},"noseLeftAlarOutTip":{"x":1166.8,"y":658.1},"noseRightAlarOutTip":{"x":1187.6,"y":655.7},"upperLipTop":{"x":1179.6,"y":667.7},"upperLipBottom":{"x":1179.6,"y":671.1},"underLipTop":{"x":1179.5,"y":674.0},"underLipBottom":{"x":1179.5,"y":678.0}},"attributes":{"headPose":{"pitch":0.0,"roll":-8.6,"yaw":2.4},"gender":"male","age":70}}]'

# qa5p
#'[{"faceId":"e09776f1-6eca-4e1d-955e-de0c581d7402","faceRectangle":{"top":816,"left":1239,"width":115,"height":115},"faceLandmarks":{"pupilLeft":{"x":1273.2,"y":848.3},"pupilRight":{"x":1323.8,"y":850.6},"noseTip":{"x":1295.6,"y":875.7},"mouthLeft":{"x":1265.8,"y":895.9},"mouthRight":{"x":1323.4,"y":899.8},"eyebrowLeftOuter":{"x":1258.6,"y":849.3},"eyebrowLeftInner":{"x":1288.3,"y":841.9},"eyeLeftOuter":{"x":1265.3,"y":850.3},"eyeLeftTop":{"x":1273.8,"y":846.2},"eyeLeftBottom":{"x":1274.0,"y":851.0},"eyeLeftInner":{"x":1281.8,"y":849.5},"eyebrowRightInner":{"x":1310.9,"y":843.0},"eyebrowRightOuter":{"x":1341.6,"y":854.6},"eyeRightInner":{"x":1315.5,"y":851.5},"eyeRightTop":{"x":1323.8,"y":848.5},"eyeRightBottom":{"x":1323.4,"y":853.6},"eyeRightOuter":{"x":1331.6,"y":853.3},"noseRootLeft":{"x":1291.6,"y":850.7},"noseRootRight":{"x":1303.7,"y":851.6},"noseLeftAlarTop":{"x":1286.6,"y":865.1},"noseRightAlarTop":{"x":1307.0,"y":866.2},"noseLeftAlarOutTip":{"x":1279.2,"y":874.9},"noseRightAlarOutTip":{"x":1313.9,"y":876.4},"upperLipTop":{"x":1295.5,"y":891.8},"upperLipBottom":{"x":1295.0,"y":895.7},"underLipTop":{"x":1292.8,"y":909.0},"underLipBottom":{"x":1292.8,"y":914.2}},"attributes":{"headPose":{"pitch":0.0,"roll":4.3,"yaw":-1.2},"gender":"male","age":31}}]'
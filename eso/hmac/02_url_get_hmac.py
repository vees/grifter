# -*- coding: utf-8 -*-

import json
import hmac
import hashlib
import base64
import random
import datetime

from eso.base32 import base32
import binascii


# /sy4s/hhgaf4f3rabe00vbpbj5taqg4m/1024/1024/180/90/?signature=

bin=binascii.unhexlify('8c60a791e3c296e0036bb2e45d2af025')
ascii=base32.b32encode(bin)
print ascii
# hhgaf4f3rabe00vbpbj5taqg4m

hmackey = "oldmcdonaldhadafarm"
originalurl = '/sy4s/hhgaf4f3rabe00vbpbj5taqg4m/1024/1024/180/90/'
binhmac = hmac.new(hmackey, originalurl, digestmod=hashlib.sha256).digest()
b64sig = base64.b64encode(binhmac)
# 'MZ+oVGKnQCsPXrF2QdoPzw5cg/8ixXJdwGG9mf7agEE='
b32sig = base32.b32encode(binhmac)
# '66ftgn32mx02p3typ5v43pgfsw75s0zz4b2q4qe0c6yskzptg10g'
stamp = datetime.datetime.utcnow().isoformat()
import urllib
finalurl = originalurl + '?' + urllib.urlencode({ 'signature': b32sig, 'timestamp': stamp })
finalurl

signedpayload=json.dumps({'numberlist':numberlist,'signature': calchmac})

print signedpayload

signedpayload2=json.loads(signedpayload)
payload2 = json.dumps(signedpayload2["numberlist"], indent=4)
calchmac2 = base64.b64encode(hmac.new(hmackey, payload2, digestmod=hashlib.sha256).digest())

print calchmac
print calchmac2

#recalchmac=base64.b64encode(hmac.new(hmackey, payload, digestmod=hashlib.sha256).digest())

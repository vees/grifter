# -*- coding: utf-8 -*-

import json
import hmac
import hashlib
import base64
import random

numberlist = list(range(1,100))
random.shuffle(numberlist)
payload = json.dumps(numberlist, indent=4)
hmackey = "oldmcdonaldhadafarm"
calchmac = base64.b64encode(hmac.new(hmackey, payload, digestmod=hashlib.sha256).digest())

signedpayload=json.dumps({'numberlist':numberlist,'signature': calchmac})

print(signedpayload)

signedpayload2=json.loads(signedpayload)
payload2 = json.dumps(signedpayload2["numberlist"], indent=4)
calchmac2 = base64.b64encode(hmac.new(hmackey, payload2, digestmod=hashlib.sha256).digest())

print(calchmac)
print(calchmac2)

#recalchmac=base64.b64encode(hmac.new(hmackey, payload, digestmod=hashlib.sha256).digest())

# -*- coding: utf-8 -*-

from exo.models import ContentSignature
from eso.base32 import base32
import binascii

cs=ContentSignature.objects.get(md5=binascii.hexlify(base32.b32decode('17k67p9rh1nt8yt0vtdkdfmwy4')))
cs.content_key.key

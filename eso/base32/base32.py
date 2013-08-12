#!/usr/bin/env python
# -*- coding: ascii -*-

"""
Module Base32
Using Douglas Crockford's Base32 scheme on top of base64 module's version.
I want my URLs to be in lowercase, and Crockford works better in typical web
font by excluding the commonly confused I and L combination, while RFC 4648
base32 does not.
Thanks to ingydotnet for https://github.com/ingydotnet/crockford-py

"""
import base64, string, hashlib, binascii

#base64.b32encode(hashlib.md5('test').digest())[:-6].translate(string.maketrans("ABCDEFGHIJKLMNOPQRSTUVWXYZ234567","0123456789ABCDEFGHJKMNPQRSTVWXYZ"),"=").lower()

# translate fails on unicode strings if maketrans object is not also unicode
__std2crock = string.maketrans(
    u"ABCDEFGHIJKLMNOPQRSTUVWXYZ234567",
    u"0123456789ABCDEFGHJKMNPQRSTVWXYZ"
).decode("latin-1")

__crock2std = string.maketrans(
    u"0123456789ABCDEFGHJKMNPQRSTVWXYZ",
    u"ABCDEFGHIJKLMNOPQRSTUVWXYZ234567"
).decode("latin-1")

def b32encode(s):
    return base64.b32encode(s).translate(__std2crock, '=').lower()

def b32decode(b32, casefold=None, map01=None):
    # Ensure the manatory padding is correct:
    b32=b32.upper()
    b32 += '=' * ((8 - len(b32) % 8) % 8)
    b32=b32.translate(__crock2std)
    return base64.b32decode(b32,casefold=casefold, map01=map01)

def test():
    binline = hashlib.md5('hello world').digest()
    encoded = b32encode(binline)
    print encoded
    decoded = b32decode(encoded)
    assert binline == decoded, "Encode and decode values do not match"

if __name__ == '__main__':
    test()

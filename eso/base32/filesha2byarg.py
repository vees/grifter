#!/usr/bin/env python
# -*- coding: ascii -*-

import hashlib
from . import base32

"""
Open a file by name, find the SHA2 value and Base32 that to produce the output.
This is just a fragile prototype.
"""

print(base32.b32encode(hashlib.sha256(open('filesha2byarg.py', 'rb').read()).digest()))


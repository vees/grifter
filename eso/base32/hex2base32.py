#!/usr/bin/env python
# -*- coding: ascii -*-

import base32
import binascii

if __name__ == '__main__':
	bin=binascii.unhexlify('6bc569718546721b1035c909ab864cbc')
	ascii=base32.b32encode(bin)
	print ascii

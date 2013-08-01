import base32
import binascii

with open('/home/rob/findmatchmd5.txt') as f:
	lines=f.read().splitlines()

for line in lines:
	binline = binascii.a2b_hex(line)
	encoded = base32.b32encode(binline)
	decoded = base32.b32decode(encoded)
	print line,encoded,decoded.encode('hex')


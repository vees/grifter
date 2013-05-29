import binascii,base32

longest=0
long_a=''
long_b=''
with open('/home/rob/findmatchmd5.txt') as f:
	lines=f.read().splitlines()

lines = [base32.b32encode(binascii.a2b_hex(line)) for line in lines]

for n in range(0,len(lines)-1):
	for i in reversed(range(longest, 32)):
		if (lines[n][0:i]==lines[n+1][0:i]):
			longest=i
			long_a=lines[n]
			long_b=lines[n+1]
			if longest==5:
				print longest, long_a, long_b
			break
#print longest, long_a, long_b


import sys
import os
import string
import random
import urllib

ALPHABET = "0123456789abcdefghjkmnpqrstvwxyz"
ALPHABET_REVERSE = dict((c, i) for (i, c) in enumerate(ALPHABET))
BASE = len(ALPHABET)

def fetch_link(uri):
	n=num_decode(uri)
	try:
		return Shortlink.objects.get(pk=n).location
	except:
		return False

def set_link(url):
	try:
		url = urllib.urlopen(url).geturl()
	except:
		return False
	existing = Shortlink.objects.filter(location=url)
	if len(existing) > 0:
		return num_encode(existing[0].pk)
	pktries=0
	while pktries<100:
		pk=random.randint(3907,242234)
		if len(Shortlink.objects.filter(pk=pk)) == 0:
			break
		pktries+=1
	try:
		link=Shortlink()
		link.pk=pk
		link.location=url
		link.save()
	except:
		return False
	return num_encode(pk)

def num_encode(n):
	i=0
	baseone = 0
	while True:
		 baseone += BASE**i
		 if ((baseone + BASE**(i+1)) > n):
			 n-=baseone
			 break 
		 i=i+1
	s = []
	while True:
		n, r = divmod(n, BASE)
		s.append(ALPHABET[r])
		if n == 0: break
	if len(s) < i+1:
		s.append(ALPHABET[0]*(1+i-len(s)))
	return ''.join(reversed(s))

def num_decode(s):
	n = 0
	for c in s:
		n = n * BASE + (ALPHABET_REVERSE[c]+1)
	return n

#for i in range(1,(BASE+1)**3):
#	print i, num_encode(i), num_decode(num_encode(i))


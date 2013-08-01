#!/usr/bin/env python
# -*- coding: ascii -*-

"""
Find duplicate files from a file in the format:
4461e8920a8e541b2a065799602c67f1  /media/dev/photos/santa2k2/dscn9694.jpg
or a call to find . -type f -exec md5sum \{} \;
and output a duplicate if the md5 hash has already been seen.
Give preference to shorter total file path length.
"""

import re
import sys

def print_dupline(a,b):
	#print a + " duplicates " + b
	print "rm " + a

def dedupe(filename):
	duplist = {}
	p = re.compile('^([0-9a-f]*)\ \ (.*)$')
	with open(filename) as f:
		for line in f:
			a = p.findall(line)[0]
			if a[0] in duplist:
				if len(a[1]) < len(duplist[a[0]]):
					print_dupline(duplist[a[0]], a[1])
					duplist[a[0]] = a[1]
				else:
					print_dupline(a[1], duplist[a[0]])
			else:
				duplist[a[0]]=a[1]

def test():
	s = '4461e8920a8e541b2a065799602c67f1  /media/dev/photos/santa2k2/dscn9694.jpg'
	p = re.compile('^([0-9a-f]*)\ \ (.*)$')
	a = p.findall(s)
	print a

if __name__ == '__main__':
	dedupe(sys.argv[1])


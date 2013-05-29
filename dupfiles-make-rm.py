import re

s = '4461e8920a8e541b2a065799602c67f1  /media/dev/photos/santa2k2/dscn9694.jpg'
p = re.compile('^([0-9a-f]*)\ \ (.*)$')
m = p.match(s)
a = p.findall(s)
print a

#import sys
#sys.exit()

duplist = {}

def print_dupline(a,b):
	#print a + " duplicates " + b
	print "rm " + a

f = open('/home/rob/photos-md5-desc.txt')
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


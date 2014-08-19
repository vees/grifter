import random

def randid():
	"""Creates a random ID space with three modified
base32 characters and one number in random order for
example vnt5, z2aa, tb9h or 2qxd""" 
	r = lambda h: h[random.randint(0,len(h))-1]
	l=[chr(x) for x in range(97,123) if chr(x) not in list("ilou")]
	n=[chr(x) for x in range (48,58)]
	e=[r(l) for x in range(3)] + [r(n)]
	random.shuffle(e)
	return e

# Prints ten examples of the same
for n in range(10):
	print "".join(randid())

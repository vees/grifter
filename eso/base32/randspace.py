import random
import string 

CROCKFORD_CHARS = list(set(string.ascii_lowercase) - set('ilou'))

def randid():
	"""Creates a random ID space with three modified
	base32 characters and one number in random order for
	example vnt5, z2aa, tb9h or 2qxd""" 
	e = [ random.choice(CROCKFORD_CHARS) for i in xrange(3) ] + \
		[ random.choice(string.digits) for i in xrange(1) ]
	random.shuffle(e)
	return ''.join(e)

# Prints ten examples of the same
for n in range(10):
	print "".join(randid())

import random

def randid():
	"""Creates a random ID space with three modified
base32 characters and one number in random order""" 
	l=[chr(x) for x in range(97,97+26) if chr(x) not in list("ilou")]
	n=[chr(x) for x in range (48,58)]
	e=[l[random.randint(0,len(l)-1)] for x in range(3)]
	e+=[n[random.randint(0,len(n)-1)]]
	random.shuffle(e)
	return e

# Prints ten examples of the same
for n in range(10):
	print "".join(randid())

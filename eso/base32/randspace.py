#!/usr/bin/env python
# -*- coding: ascii -*-

'''
Tools for generating unique four character urls
'''

import random
import string 

CROCKFORD_CHARS = list(set(string.ascii_lowercase) - set('ilou'))

def randid():
	"""Creates a random ID space with three modified
	base32 characters and one number in random order for
	example vnt5, z2aa, tb9h or 2qxd""" 
	e = [ random.choice(CROCKFORD_CHARS) for i in range(3) ] + \
		[ random.choice(string.digits) for i in range(1) ]
	random.shuffle(e)
	return ''.join(e)

def randids(n):
    """Creates a list of n random id""" 
    if n<=0:
        raise ValueError("Value must be greater than 1")
    return [randid() for x in range(0,n)]

if __name__ == "__main__":
    print((randids(11)))

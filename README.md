Narthex Project

Yet another content management system.

This one is going to be located at vees.net so we're designing around 
urls that fit a short URL format and are "cool urls" that don't change 
over time.

# URL Structure

For example we will have a picture with a perm URL and a short URL. 
Using an image file with a base64 encoded SHA-2 and MD5, base32 
encoded MD5 and then truncated to 4 characters.

	https://vees.net/218c1e394...(48)...578570df
	https://vees.net/218c/

	https://vees.net/4661wea9q...(36)...8nw5e3fg
	https://vees.net/4661/

	https://vees.net/32c1a215b9d342e657b3046294952176
	https://vees.net/32c1/

	https://vees.net/mcwwsjjjqvg28q9k5y0pt8bfkr
	https://vees.net/mcww/

In either case the shortened bit space will be 32^n where n is the 
number of characters.

    >>> for i in range(1,6): print i,``i**32``;
    ... 
    1 32
    2 1024
    3 32768
    4 1048576
    5 33554432

As the number of image files on the site is around 45,000 over ten 
years, we can expect about 10 times as many non image files and an 
expansion of 100% over the next ten, we are reasonably bounded by the 
4 character space for 990,000 expected files.

A four character space has two problems collision space of the MD5 
and SHA-2 hashes, and keeping file URLs short and constant while 
leaving space for reserved functional URLs.

For example, already the vees.net domain has the following space 
reserved for file management:

    https://vees.net/file/
	https://vees.net/meta/
	https://vees.net/tags/
	https://vees.net/slug/

And also for an unrelated application and API space:

	https://vees.net/apps/

And several legacy static site URLs:

    https://vees.net/g2/
    https://vees.net/scanner/
    https://vees.net/resume/
    
A run in 2013 of the MD5 space of the 45,000 image files found a 
collision at the 7th character of the base-32 encoded version 
starting from the first bit.

There are a few strategies for mitigating collisions with short 
space hashes. Most of these do not allow the hash space to be 
recreated from the same set of files if the file set has been added 
to over time. For instance the Maryland Drivers License system has a 
collision-prone system using soundex of names and hashing of 
birthdays to create a unique ID and resolves collisions with the 
following rule:

	In the event of two or more people having identical driver's 
	licence numbers, this final group of digits will be used to 
	differeniate them. Simple add one to the final group of digits 
	until you find an unused entry.

Source [High Programmer](http://4ve.es/JyO)

The best intersecting solution appears to be the following:

Create a four character file ID using the base32-encoded SHA-2 hash or 
from a random 128 bit space.

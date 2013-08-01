import os
import glob
from regatta.models import Picture, Moment, PictureSimple
import EXIF
import itertools
from datetime import datetime
import hashlib

def exim_fetch(filename):
	output = "None"
	try:
		f = open(filename, 'rb')
		tags = EXIF.process_file(f)
		output = str(tags['Image Orientation'])
	except:
		otuput = "Exception"
	finally:
		f.close()
	return output

def exim_tags(filename):
	f = open(filename, 'rb')
	return EXIF.process_file(f)

directory="/local/photos/sd600-20090906"
pix=PictureSimple.objects.filter(directory=directory) #, filename="IMG_6952.JPG")
#pic=pix[0]
for pic in pix:
	print pic.directory, pic.filename, exim_fetch(pic.directory+"/"+pic.filename)
#tags = exim_tags(pic.directory+"/"+pic.filename)



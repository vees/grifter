import os
import glob
from regatta.models import Picture, Moment, PictureSimple
import EXIF
import itertools
from datetime import datetime
import hashlib
from PIL import Image

def exif_fetch(filename):
	output = "None"
	try:
		f = open(filename, 'rb')
		tags = EXIF.process_file(f)
		output = str(tags['Image Orientation'])
	except:
		output = "Exception"
	finally:
		f.close()
	return output

def exif_tags(filename):
	f = open(filename, 'rb')
	return EXIF.process_file(f)

def original_dimensions(filename):
	im = Image.open(filename)
	return im.size

def exif_translate(text):
	if text=="Rotated 90 CW":
		return 90
	if text=="Rotated 90 CCW":
		return 270
	if text=="Horizontal (normal)":
		return 0
	return None

def dimensions_translate(size):
	(width,height) = size;
	if (height>width):
		return 90
	return 0

def rotation_guess(er, dr):
	if er==90:
		return 90
	if er==270:
		return 270
	if dr==90:
		return 180 # means rotated, but we're not sure what direction
	return 0 # Means landscape

#directory="/local/photos/jan04random"
#pix=PictureSimple.objects.filter(directory=directory)
pix=PictureSimple.objects.all()
for pic in pix:
	if (pic.legacy):
		size = original_dimensions(
			"/local/img/" + pic.legacy.theme.directory + "/" + pic.legacy.filename + ".jpg")
	else:
		size = original_dimensions( pic.directory+"/"+pic.filename)	
	er = exif_translate(exif_fetch(pic.directory+"/"+pic.filename))
	dr = dimensions_translate(size)
	pic.rotation=rotation_guess(er,dr)
	pic.save()
	print "Saved", pic.directory, pic.filename, rotation_guess(er,dr)


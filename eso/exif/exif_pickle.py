import os
import glob
from regatta.models import Picture, Moment, PictureSimple
from . import EXIF
import itertools
from datetime import datetime
import hashlib

path = '/media/dev/photos'

def exim_fetch(filename):
	f = open(filename, 'rb')
	tags = EXIF.process_file(f)
	timelist = [ item.split(':') for item in str(tags['EXIF DateTimeOriginal']).split(' ') ] 
	timelist = list(itertools.chain(*timelist))
	timelist = [ int(item) for item in timelist ]
	return tags

tags = exim_fetch('/media/dev/photos/sd600-20100705/IMG_9408.JPG')


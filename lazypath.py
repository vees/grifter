import os
import glob
from regatta.models import Picture, Moment
import EXIF
import itertools
from datetime import datetime


path = '/home/rob/photos'

def exim_fetch(filename):
	f = open(filename, 'rb')
	tags = EXIF.process_file(f)
	test = [ item.split(':') for item in str(tags['EXIF DateTimeOriginal']).split(' ') ] 
	test = list(itertools.chain(*test))
	test = [ int(item) for item in test ]
	when = datetime(test[0], test[1], test[2], test[3], test[4], test[5])
	return when

def import_images(dirname):
	for f in os.listdir(dirname):
		fullpath = os.path.join(dirname, f)
		if os.path.isfile(fullpath):
			print os.path.splitext(f)[1]
			if os.path.splitext(f)[1] in [".jpg",".JPG"]:
				p=Picture()
				p.directory=dirname
				p.filename=f
				m=Moment()
				m.ctime = datetime.fromtimestamp(os.stat(fullpath).st_ctime)
				m.exim = exim_fetch(fullpath)
				m.save()
				p.taken_on=m
				print "saved" + dirname + " and " + f 
				p.save()
		if os.path.isdir(fullpath):
			import_images(fullpath)

import_images(path)

#for infile in glob.glob( os.path.join(path, '*.JPG' ) ):
#	print("current file is: " + infile)

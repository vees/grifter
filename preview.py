import os
import glob
#from regatta.models import Picture, Moment
import EXIF
import itertools
from datetime import datetime
import hashlib

path = '/home/rob/photos'

def exim_fetch(filename):
	try:
		f = open(filename, 'rb')
		content = f.read()
		md5hash = hashlib.md5(content).hexdigest()
		f.seek(0)
		tags = EXIF.process_file(f)
		timelist = [ item.split(':') for item in str(tags['EXIF DateTimeOriginal']).split(' ') ] 
		timelist = list(itertools.chain(*timelist))
		timelist = [ int(item) for item in timelist ]
		try:
			when = datetime(timelist[0], timelist[1], timelist[2], timelist[3], timelist[4], timelist[5])
		except ValueError:  # When 0000:00:00 00:00:00
			return str(tags['EXIF DateTimeOriginal'])
		return str(when), md5hash
	except KeyError:
		return '','',''

def import_images(dirname):
	for f in os.listdir(dirname):
		fullpath = os.path.join(dirname, f)
		if os.path.isfile(fullpath):
			#print os.path.splitext(f)[1]
			if os.path.splitext(f)[1] in [".jpg",".JPG"]:
				print fullpath, datetime.fromtimestamp(os.stat(fullpath).st_mtime), exim_fetch(fullpath)
		if os.path.isdir(fullpath):
			import_images(fullpath)

try:
	import_images(path)
except KeyboardInterrupt:
	print "Done."
	exit

#for infile in glob.glob( os.path.join(path, '*.JPG' ) ):
#	print("current file is: " + infile)

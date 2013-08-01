import os
import glob
from regatta.models import Picture, Moment
import EXIF
import itertools
from datetime import datetime
import hashlib

path = '/local/photos'

def exim_fetch(filename):
	try:
		f = open(filename, 'rb')
		tags = EXIF.process_file(f)
		timelist = [ item.split(':') for item in str(tags['EXIF DateTimeOriginal']).split(' ') ] 
		timelist = list(itertools.chain(*timelist))
		timelist = [ int(item) for item in timelist ]
		try:
			when = datetime(timelist[0], timelist[1], timelist[2], timelist[3], timelist[4], timelist[5])
		except ValueError:  # When 0000:00:00 00:00:00
			return str(tags['EXIF DateTimeOriginal'])
		return str(when)
	except KeyError:
		return ''
	finally:
		f.close()

def md5_parse(filename):
	try:
		f = open(filename, 'rb')
		content = f.read()
		md5hash = hashlib.md5(content).hexdigest()
		return md5hash
	except ValueError:
		return 'No hash'
	finally:
		f.close()
	

def import_images(dirname):
	for f in os.listdir(dirname):
		fullpath = os.path.join(dirname, f)
		if os.path.isfile(fullpath):
			#print os.path.splitext(f)[1]
			if os.path.splitext(f)[1] in [".jpg",".JPG"]:
				print fullpath, datetime.fromtimestamp(os.stat(fullpath).st_mtime), datetime.fromtimestamp(os.stat(fullpath).st_ctime), exim_fetch(fullpath), md5_parse(fullpath)
				print fullpath, create_moment(datetime.fromtimestamp(os.stat(fullpath).st_mtime), datetime.fromtimestamp(os.stat(fullpath).st_ctime), exim_fetch(fullpath)), md5_parse(fullpath)

		if os.path.isdir(fullpath):
			import_images(fullpath)

def create_moment( mtime, ctime, exim):
	m = Moment()
	try:
		m.mtime = mtime
	except:
		pass
	try:
		m.ctime = ctime
	except:
		pass
	try:
		m.exim = exim
	except:
		pass
	try:
		m.save()
	except:
		pass
	return m.mtime, m.ctime, m.exim

try:
	import_images(path)
except KeyboardInterrupt:
	print "Done."
	exit

#for infile in glob.glob( os.path.join(path, '*.JPG' ) ):
#	print("current file is: " + infile)

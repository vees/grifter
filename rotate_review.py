import os
import glob
from regatta.models import Picture, Moment, PictureSimple
import EXIF
import itertools
from datetime import datetime
import hashlib
from PIL import Image

for rotation in [0,90,180,270]:
	ps=PictureSimple.objects.filter(rotation=rotation)
	print rotation, ps.count()
	for p in ps:
		print p.id,p.directory,p.filename


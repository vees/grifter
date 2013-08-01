# Create your views here.
from PIL import Image
import StringIO
from exo.models import Picture, Old_Picture, PictureSimple
from django.http import HttpResponse
from django.conf import settings
from random import Random
from django.shortcuts import render_to_response

def connect(request, original, new):
	np = PictureSimple.objects.get(pk=new)
	op = Old_Picture.objects.get(pk=original)
	np.old_id = op
	np.save()
	nextid = Old_Picture.objects.filter(id__gt=original)[0].id
	return index(request, nextid)

def index(request, image_id):
	op = Old_Picture.objects.get(pk=image_id)
	print op.filename
	newpics = PictureSimple.objects.filter(filename=op.filename+".jpg", old_id__isnull=True)
	ids_greater = Old_Picture.objects.filter(id__gt=image_id)
	nextid = ids_greater[0].id
	#remaining = float(ids_greater.count())/Old_Picture.objects.count()
	remaining = float(ids_greater.count())
	remaining = round(remaining/60.0, 2)
	return render_to_response("picture-sync.html", 
		{ 'oldpicture': op, 'newpics': newpics, 'nextid': nextid,
			'remaining': remaining })

def image(request, image_id):
	p=Picture.objects.get(pk=image_id)
	return HttpResponse(
		image_it(p.directory+"/"+p.filename),
		mimetype="image/jpeg"
		)

def thumbnail_new(request, image_id):
	p=PictureSimple.objects.get(pk=image_id)
	return HttpResponse(
		thumbnail_it(p.directory+"/"+p.filename),
		mimetype="image/jpeg"
		)

def thumbnail_old(request, image_id):
	p=Old_Picture.objects.get(pk=image_id)
	return HttpResponse(
		thumbnail_it("/local/img/"+p.theme.directory+"/"+p.filename+".jpg"),
		mimetype="image/jpeg"
		)

def thumbnail_it(path_to_original):
	im = Image.open(path_to_original)
	size = 240,180
	im.thumbnail(size, Image.ANTIALIAS)
	buf= StringIO.StringIO()
	im.save(buf, format= 'JPEG')
	return buf.getvalue()

def image_it(path_to_original):
	im = Image.open(path_to_original)
	size = 500,375,180
	im.thumbnail(size, Image.ANTIALIAS)
	buf= StringIO.StringIO()
	im.save(buf, format= 'JPEG')
	return buf.getvalue()


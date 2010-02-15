# Create your views here.
from PIL import Image
import StringIO
from regatta.models import Picture, Old_Picture
from django.http import HttpResponse
from random import Random
from django.shortcuts import render_to_response

def index(request, image_id):
	forward=get_picture_id_random()
	backward=get_picture_id_random()
	current=image_id
	return render_to_response(
		'random-off.html',
		{
			'forward': forward,
			'backward': backward,
			'current': current,
		} 
	)

def image(request, image_id):
	p=Picture.objects.get(pk=image_id)
	return HttpResponse(
		image_it(p.directory+"/"+p.filename),
		mimetype="image/jpeg"
		)

def thumbnail(request, image_id):
	p=Picture.objects.get(pk=image_id)
	return HttpResponse(
		thumbnail_it(p.directory+"/"+p.filename),
		mimetype="image/jpeg"
		)

def get_picture_id_random():
	g=Random()
	return g.randint(1,Picture.objects.count())

def get_picture_id_randomold():
	g=Random()
	return g.randint(1,Old_Picture.objects.count())

def random(request):
	g=Random()
	p=Picture.objects.get(pk=g.randint(1,Picture.objects.count()))
	return HttpResponse(
		thumbnail_it(p.directory+"/"+p.filename),
		mimetype="image/jpeg"
		)

def randomold(request):
	g=Random()
	p=Old_Picture.objects.get(pk=g.randint(1,Old_Picture.objects.count()))
	return HttpResponse(
		thumbnail_it('/local/img/'+p.theme.directory+"/"+p.filename+'.jpg'),
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


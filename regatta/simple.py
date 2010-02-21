# Create your views here.
from PIL import Image
import StringIO
from regatta.models import PictureSimple
from django.http import HttpResponse
from random import Random
from django.shortcuts import render_to_response

def index(request, image_id):
	forward=get_picture_id_forward(image_id)
	backward=get_picture_id_backward(image_id)
	random=get_picture_id_random()
	current=image_id
	return render_to_response(
		'random-off.html',
		{
			'forward': forward,
			'backward': backward,
			'current': current,
			'random': random
		} 
	)

def image(request, image_id):
	p=PictureSimple.objects.get(pk=image_id)
	return HttpResponse(
		image_it(p.directory+"/"+p.filename),
		mimetype="image/jpeg"
		)

def thumbnail(request, image_id):
	p=PictureSimple.objects.get(pk=image_id)
	return HttpResponse(
		thumbnail_it(p.directory+"/"+p.filename),
		mimetype="image/jpeg"
		)

def get_picture_id_forward(image_id):
	return PictureSimple.objects.filter(pk__gt=image_id)[0].id

def get_picture_id_backward(image_id):
	return PictureSimple.objects.filter(pk__lt=image_id).order_by('-id')[0].id

def get_picture_id_random():
	g=Random()
	return g.randint(1,PictureSimple.objects.count())

def random(request):
	g=Random()
	p=Picture.objects.get(pk=g.randint(1,Picture.objects.count()))
	return HttpResponse(
		thumbnail_it(p.directory+"/"+p.filename),
		mimetype="image/jpeg"
		)

def randomold(request):
	match=0
	while 1:
		try:
			g=Random()
			p=Old_Picture.objects.get(pk=g.randint(1,Old_Picture.objects.count()))
			break
		except Old_Picture.DoesNotExist:
			pass
	return HttpResponse(
		thumbnail_it('/local/img/'+p.theme.directory+"/"+p.filename+'.jpg'),
		mimetype="image/jpeg"
		)

def thumbnail_it(path_to_original):
	im = Image.open(path_to_original)
	#size = 240,180
	size = 120,80
	im.thumbnail(size, Image.ANTIALIAS)
	buf= StringIO.StringIO()
	im.save(buf, format= 'JPEG')
	return buf.getvalue()

def image_it(path_to_original):
	im = Image.open(path_to_original)
	#size = 500,375,180
	size = 800,500,180
	im.thumbnail(size, Image.ANTIALIAS)
	buf= StringIO.StringIO()
	im.save(buf, format= 'JPEG')
	return buf.getvalue()


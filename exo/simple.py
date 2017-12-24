# Create your views here.
from PIL import Image
import io
from regatta.models import PictureSimple
from django.http import HttpResponse
from random import Random
from django.shortcuts import render_to_response
import watermark

def index(request, image_id):
	forward=get_picture_id_forward(image_id)
	backward=get_picture_id_backward(image_id)
	random=get_picture_id_random()
	current_id=image_id
	current=PictureSimple.objects.get(pk=image_id)
	if (current.legacy):
		legacy = current.legacy
	else:
		legacy = None
	return render_to_response(
		'random-off.html',
		{
			'forward': forward,
			'backward': backward,
			'current': current_id,
			'random': random,
			'legacy': legacy
		} 
	)

def hundred(request, image_id):
	hundred=PictureSimple.objects.filter(pk__gte=image_id)[0:100]
	forward = hundred[99].id
	return render_to_response(
		'hundred.html',
		{
			'hundred': hundred,
			'forward': forward,
		}
	)

def image(request, image_id):
	p=PictureSimple.objects.get(pk=image_id)
	return HttpResponse(
		image_it(p.directory+"/"+p.filename, p.rotation),
		mimetype="image/jpeg"
		)

def thumbnail(request, image_id):
	p=PictureSimple.objects.get(pk=image_id)
	return HttpResponse(
		thumbnail_it(p.directory+"/"+p.filename, p.rotation),
		mimetype="image/jpeg"
		)

def get_picture_id_forward(image_id):
	try:
		return PictureSimple.objects.filter(pk__gt=image_id)[0].id
	except IndexError:
		return None

def get_picture_id_backward(image_id):
	try:
		return PictureSimple.objects.filter(pk__lt=image_id).order_by('-id')[0].id
	except IndexError:
		return None

def get_picture_id_random():
	g=Random()
	#return g.randint(1,PictureSimple.objects.count())
	return PictureSimple.objects.all()[g.randint(1,PictureSimple.objects.count())].id

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

def thumbnail_it(path_to_original, rotation):
	im = Image.open(path_to_original)
	#size = 240,180
	#size = 120,80
	size = 240,160
	# Tips: http://www.daniweb.com/code/snippet216637.html
	im.thumbnail(size, Image.ANTIALIAS)
	if (rotation!=180):
		im = im.rotate(360-rotation)
	buf= io.StringIO()
	im.save(buf, format= 'JPEG')
	return buf.getvalue()

def image_it(path_to_original, rotation):
	im = Image.open(path_to_original)
	mark = Image.open('/home/rob/grifter/newcard-trans2.png')
	#size = 500,375,180
	size = 800,500,180
	im.thumbnail(size, Image.ANTIALIAS)
	if (rotation!=180):
		im = im.rotate(360-rotation)
	buf= io.StringIO()
	#im.save(buf, format= 'JPEG')
	out = watermark.watermark(im, mark, "scale", 0.4)
	out.save(buf, format='JPEG')
	return buf.getvalue()


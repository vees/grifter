import StringIO
import binascii

from PIL import Image
from random import Random

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.conf import settings

from exo.models import PictureSimple
from eso.base32 import base32

def random(request):
    """Given a / URL, return another URL encoded as /meta/abcdefghij which
returns a page containing an image url"""
    g=Random()
    p=PictureSimple.objects.get(pk=g.randint(1,PictureSimple.objects.count()))
    return HttpResponseRedirect("/meta/%s" % (base32.b32encode(binascii.unhexlify(p.file_hash))))

def page_by_base32(request, base32md5):
    """Return a page with an image link by base32md5 and a link back to / URL
for another load"""
    #p=PictureSimple.objects.get(file_hash=base32.b32decode(base32md5)
    return HttpResponse("<a href='/'><img src='/file/%s'></a>" % (base32md5))

def image_by_base32(request, base32md5):
    """Return a resized file by the base32md5"""
    p=PictureSimple.objects.get(file_hash=binascii.hexlify(base32.b32decode(base32md5)))
    return HttpResponse(
        image_it(p.get_local_path()),
        mimetype="image/jpeg"
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


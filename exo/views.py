import StringIO
import binascii

from PIL import Image
from random import Random

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.conf import settings
from django.template import RequestContext, loader

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

def privacy_unchecked(request):
    unchecked=PictureSimple.objects.filter(private=None)
    remaining=unchecked.count()
    pictures = unchecked[0:6]
    allbutton = ",".join([x.b32md5 for x in pictures])
    template = loader.get_template("private.html")
    context = RequestContext(request, {'pictures': pictures, 'allbutton': allbutton, 'remaining':remaining})
    return HttpResponse(template.render(context))

def update_privacy(request, actiontext, md5list):
    """Take a comma delimited string of base32 md5 plus an action text of private or public
and iterate over the results to change the status of individual images"""
    if actiontext not in ['private','public']:
        return HttpResponse("Invalid command")

    try:
        md5hexlist = [binascii.hexlify(base32.b32decode(md5)) for md5 in md5list.split(",")]
    except:
        return HttpResponse("Bad list of elements")

    for md5hex in md5hexlist:
        p=PictureSimple.objects.get(file_hash=md5hex)
        p.private = (actiontext == 'private')
        p.save()

    return HttpResponseRedirect("/")

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


# -*- coding: utf-8 -*-

from io import StringIO
import io
import binascii
import pprint

from PIL import Image

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import Http404
from django.template import RequestContext, Template, loader
from django.conf import settings
from django.db.models import Count
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from exo.models import ContentKey, ContentInstance, ContentSignature, Picture, Tag2
from eso.base32 import base32
from eso.base32 import randspace

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

import json

@login_required
def redundancy(request, offset=1):
    allsignatures = ContentSignature.objects.select_related(
        'content_key').prefetch_related('tags').prefetch_related(
        'contentinstance_set').prefetch_related(
        'contentinstance_set__content_container').annotate(
        content_instance_count=Count(
        'contentinstance')).order_by('contentinstance__id')
    paginator = Paginator(allsignatures, 1000)
    try:
        signatures = paginator.page(offset)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        signatures = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        signatures = paginator.page(paginator.num_pages)
    return render(request, "redundancy.html", {'signatures': signatures})

def random(request):
    """Given a / URL, return another URL encoded as /meta/abcdefghij which
returns a page containing an image url"""
    # If this is slow in production, use this tip instead;
    # http://stackoverflow.com/a/2118712/682915
    instance = ContentInstance.objects.filter(content_container=settings.NARTHEX_CONTAINER_ID).order_by('?').first()
    if instance:
        key = instance.content_signature.content_key.key
    else:
        return HttpResponse("No valid instances to show you, add some content first")
    return HttpResponseRedirect(reverse('page_by_contentkey', kwargs={'contentkey': key}))

def page_by_contentkey(request, contentkey):
    try:
        sig=ContentKey.objects.filter(key=contentkey).first().contentsignature_set.all().first()
        zerothfile=sig.contentinstance_set.filter(content_container=settings.NARTHEX_CONTAINER_ID).first()
        filename = "/".join([zerothfile.content_container.path,zerothfile.relpath,zerothfile.filename])
    except:
        raise Http404('No file for this key %s' % contentkey) # , content_type="text/html")
    import eso.exif.EXIF
    f = open(filename, 'rb')
    exifhash = eso.exif.EXIF.process_file(f)

    for key in list(exifhash.keys()):
        try:
            if len(str(exifhash[key])) > 50:
                del exifhash[key]
        except:
                del exifhash[key]
    exifdata = pprint.pformat(exifhash, indent=1, width=50, depth=1)
    pagetags = ContentKey.objects.filter(
        key=contentkey).first().contentsignature_set.all().first().tags.all().order_by('slug')
    description = " ".join([tag.slug for tag in pagetags])
    if not description:
        description = filename
    alltags = Tag2.objects.annotate(tagged_sig=Count('contentsignature')).order_by('-tagged_sig')
    commontags = Tag2.objects.filter(contentsignature__contentinstance__relpath=zerothfile.relpath).annotate(tagged_sig=Count('contentsignature')).order_by('-tagged_sig')
    untagged = ContentSignature.objects.annotate(tags_count=Count(
        'tags')).filter(tags_count=0).filter(contentinstance__content_container=settings.NARTHEX_CONTAINER_ID)
    try:
        nextuntagged = untagged.exclude(content_key__key=contentkey).order_by(
            'contentinstance__relpath','contentinstance__filename').first().content_key.key
        nextuntaggedurl = reverse('page_by_contentkey', kwargs={'contentkey': nextuntagged})
    except AttributeError:
        nextuntaggedurl = reverse('main_page')
    try:
        randomkey = (ContentInstance.objects
            .filter(content_container=settings.NARTHEX_CONTAINER_ID)
            .order_by('?')
            .first().content_signature.content_key.key)
        destination = reverse('page_by_contentkey', kwargs={'contentkey': randomkey})
    except AttributeError:
        destination = reverse('main_page')
    untaggedremain = untagged.count()
    context = {
        'nextuntagged': nextuntaggedurl,
        'untaggedremain': untaggedremain,
        'signature': sig,
        'commontags': commontags,
        'pagetags': pagetags,
        'alltags': alltags,
        'contentkey': contentkey,
        'description': description,
        'destination': destination,
        'imagesource': reverse('image_by_contentkey', kwargs={'contentkey': contentkey}),
        'exifdata': exifdata }
    template = loader.get_template("meta.html")
    return HttpResponse(template.render(context, request))

def image_by_contentkey(request, contentkey):
    try:
        sig = ContentKey.objects.filter(key=contentkey).first().contentsignature_set.all().first()
        zerothfile=sig.contentinstance_set.filter(content_container=settings.NARTHEX_CONTAINER_ID).first()
        filename = "/".join([zerothfile.content_container.path,zerothfile.relpath,zerothfile.filename])
        rotation=0
        if hasattr(sig, 'picture'):
            if (hasattr(sig.picture, 'rotation') and sig.picture.rotation!=None):
                rotation=360-sig.picture.rotation
    except IOError:
        filename="File not found"
    return HttpResponse(
        image_it(filename, rotation=rotation),
        content_type="image/jpeg"
        )

#def page_by_base32(request, base32md5):
#    """Return a page with an image link by base32md5 and a link back to / URL
#for another load"""
#    p=PictureSimple.objects.get(file_hash=binascii.hexlify(base32.b32decode(base32md5)))
#    import eso.exif.EXIF
#    f = open(p.get_local_path(), 'rb')
#    exifhash = eso.exif.EXIF.process_file(f)
#
#    for key in exifhash.keys():
#        try:
#            if len(str(exifhash[key])) > 50:
#                del exifhash[key]
#        except:
#                del exifhash[key]
#    exifdata = pprint.pformat(exifhash, indent=1, width=50, depth=1)
#    template = loader.get_template("meta.html")
#    context = RequestContext(request, {
#        'description': p.filename,
#        'destination': request.build_absolute_uri(reverse('exo.views.random')),
#        'imagesource': request.build_absolute_uri(reverse('exo.views.image_by_base32',args=[base32md5])),
#        'exifdata': exifdata })
#    return HttpResponse(template.render(context))

def page_by_base32(request, base32md5):
    cs=ContentSignature.objects.get(md5=binascii.hexlify(base32.b32decode(base32md5)))
    key=cs.content_key.key
    return HttpResponseRedirect(reverse('page_by_contentkey', kwargs={'contentkey': key}))

def image_by_base32(request, base32md5):
    cs=ContentSignature.objects.get(md5=binascii.hexlify(base32.b32decode(base32md5)))
    key=cs.content_key.key
    return HttpResponseRedirect(reverse('image_by_contentkey', kwargs={'contentkey': key}))

#def privacy_unchecked(request):
#    batchsize=24
#    unchecked=PictureSimple.objects.filter(private=None).order_by('directory','filename')
#    remaining=unchecked.count()/batchsize
#    pictures = unchecked[0:batchsize]
#    allbutton = ",".join([x.b32md5 for x in pictures])
#    template = loader.get_template("private.html")
#    context = RequestContext(request, {'pictures': pictures, 'allbutton': allbutton, 'remaining':remaining})
#    return HttpResponse(template.render(context))
#
#def update_privacy(request, actiontext, md5list):
#    """Take a comma delimited string of base32 md5 plus an action text of private or public
#and iterate over the results to change the status of individual images"""
#    if actiontext not in ['private','public','reset']:
#        return HttpResponse("Invalid command")
#
#    try:
#        md5hexlist = [binascii.hexlify(base32.b32decode(md5)) for md5 in md5list.split(",")]
#    except:
#        return HttpResponse("Bad list of elements")
#
#    privacy=None
#    if actiontext=='private':
#        privacy=1
#    if actiontext=='public':
#        privacy=0
#
#    PictureSimple.objects.filter(file_hash__in=md5hexlist).update(private = privacy)
#
#    return HttpResponseRedirect("/")

def image(request, image_id):
    p=Picture.objects.get(pk=image_id)
    return HttpResponse(
        image_it(p.directory+"/"+p.filename),
        content_type="image/jpeg"
        )

def thumbnail(request, image_id):
    p=Picture.objects.get(pk=image_id)
    return HttpResponse(
        thumbnail_it(p.directory+"/"+p.filename),
        content_type="image/jpeg"
        )

#def randomold(request):
#    match=0
#    while 1:
#        try:
#            g=Random()
#            p=Old_Picture.objects.get(pk=g.randint(1,Old_Picture.objects.count()))
#            break
#        except Old_Picture.DoesNotExist:
#            pass
#    return HttpResponse(
#        thumbnail_it('/local/img/'+p.theme.directory+"/"+p.filename+'.jpg'),
#        content_type="image/jpeg"
#        )

def thumbnail_it(path_to_original):
    im = Image.open(path_to_original)
    size = 240,180
    im.thumbnail(size, Image.ANTIALIAS)
    buf= StringIO.StringIO()
    im.save(buf, format= 'JPEG')
    return buf.getvalue()

def image_it(path_to_original, rotation=0):
    im = Image.open(path_to_original)
    if rotation!=0:
        im=im.rotate(rotation)
    size = 1024,1024,180
    im.thumbnail(size, Image.ANTIALIAS)
    buf= io.BytesIO()
    im.save(buf, format= 'JPEG')
    return buf.getvalue()

def new_id(request):
    payload={'id': randspace.randid()}
    response=json.dumps(payload, indent=4)
    return HttpResponse(response, content_type="application/json")

def remaining_id_space(request):
    total=22**3*10*4
    used=ContentKey.objects.all().count()
    remaining=total-used
    capacity=int(ContentKey.objects.all().count()/(float(total))*100)
    payload={'total': total, 'used': used, 'remaining': remaining, 'capacity': capacity}
    response=json.dumps(payload, indent=4)
    return HttpResponse(response, content_type="application/json")

class MyEncoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__

def export(request):
    ci=ContentInstance.objects.select_related().prefetch_related('content_signature__content_key').first()
    response = json.dumps(ci, cls=MyEncoder, sort_keys=True, indent=4)
    return HttpResponse(response, content_type="application/json")

def addrotation(key, rotation):
    sig=ContentKey.objects.filter(key=key).first().contentsignature_set.all().first()
    p,new=Picture.objects.update_or_create(signature=sig, defaults={'rotation': rotation})
    return sig,p.rotation,new

def addrating(key, rating):
    sig=ContentKey.objects.filter(key=key).first().contentsignature_set.all().first()
    p,new=Picture.objects.update_or_create(signature=sig, defaults={'rating': rating})
    return sig,p.rotation,new

def addtag(key, tags):
    sig=ContentKey.objects.filter(key=key).first().contentsignature_set.all().first()
    for tag in tags.split(","):
        t,created=Tag2.objects.update_or_create(slug=tag)
        sig.tags.add(t)

@login_required
def api_action(request, contentkey, action, attribute=''):
    try:
        if attribute=='':
            attribute=request.GET.get('attribute')
        if action=='rotate':
            addrotation(contentkey,attribute)
        if action=='rating':
            addrating(contentkey,attribute)
        if action=='tag':
            addtag(contentkey,attribute)
    except:
        pass

    payload=(contentkey, action, attribute)
    response=json.dumps(payload, indent=4)
    return HttpResponse(response, content_type="application/json")

def api_tagdump(request):
    tagdump = dict([(t.slug, [s.sha2 for s in t.contentsignature_set.all()]) for t in Tag2.objects.order_by('slug')])
    response = json.dumps(tagdump, indent=4)
    return HttpResponse(response, content_type="application/json")

@csrf_exempt
@login_required
def api_tagload(request):
    '''
    This function might be more efficient if the dictionary were inverted,
    and also we can pre-check with
    [a.sha2 for a in Tag2.objects.filter(slug='playadelfuego').first().contentsignature_set.all()]
    for a slug name and save our selves some loading time (later)
    '''
    ignored=0
    nomatch=0
    added=0
    posted=json.loads(request.body)
    for tag,shalist in posted.items():
        print(tag)
        t,created=Tag2.objects.update_or_create(slug=tag)
        sha2ignore = set([a.sha2 for a in Tag2.objects.filter(slug=tag).first().contentsignature_set.all()])
        ignored=len(sha2ignore)
        for sha2 in set(shalist) - sha2ignore:
            sig=ContentSignature.objects.filter(sha2=sha2).first()
            if not sig:
                nomatch+=1
            else:
                sig.tags.add(t)
                sig.save()
                added+=1
    return HttpResponse(json.dumps({'ignored':ignored,'added':added,'nomatch':nomatch}), content_type="application/json")

def api_rotatedump(request):
    rotatedump = {'0': [], '90': [], '180': [], '270': []}
    for p in Picture.objects.filter(rotation__isnull=False).prefetch_related('signature'):
        rotation = str(p.rotation)
        rotatedump[rotation] += [p.signature.sha2]
    response = json.dumps(rotatedump, indent=4)
    return HttpResponse(response, content_type="application/json")


@csrf_exempt
@login_required
def api_rotateload(request):
    ignored=0
    nomatch=0
    added=0
    addlist=[]
    posted=json.loads(request.body)
    for rotation,sha2list in posted.items():
        skipsig = set([p.signature.sha2 for p in Picture.objects.filter(rotation=rotation).prefetch_related('signature')])
        ignored=len(skipsig)
        for sha2 in set(sha2list) - skipsig:
            sig = ContentSignature.objects.filter(sha2=sha2).first()
            if not sig:
                nomatch+=1
            else:
                Picture.objects.update_or_create(signature=sig, defaults={'rotation': rotation})
                added+=1
                addlist+=[sig.sha2]
    return HttpResponse(json.dumps({'ignored':ignored,'added':added,'nomatch':nomatch,'addlist':addlist}), content_type="application/json")

def taglist(request):
    try:
        toptags=Tag2.objects.annotate(tagged_sig=Count('contentsignature')).order_by('-tagged_sig')[0:9]
        alltags=Tag2.objects.order_by('slug')
    except:
        raise Http404
    template = loader.get_template("alltags.html")
    context = {
        'toptags': toptags,
        'alltags': alltags }
    return HttpResponse(template.render(context, request))

def tagbyslug(request,slug):
    try:
        tagdict = dict([(sig.content_key.key, " ".join([t.slug for t in sig.tags.order_by('slug')])) for sig in Tag2.objects.get(slug=slug).contentsignature_set.all()])
    except:
        raise Http404
    template = loader.get_template("tags.html")
    context = {
        'slug': slug,
        'tagdict': tagdict }
    return HttpResponse(template.render(context, request))

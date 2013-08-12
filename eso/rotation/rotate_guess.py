import os
import glob
import itertools
import hashlib

from datetime import datetime
from PIL import Image

import eso.exif.EXIF
from exo.models import Picture, Moment, PictureSimple
from django.conf import settings

path = settings.NARTHEX_PHOTO_PATH

class ExifReduced:
    def __init__(self, exiftags):
        self._rotation = str(exiftags['Image Orientation'])
        self._cameratype = str(exiftags['Image Model'])

    def __unicode__(self):
        return "Camera: %s, Rotation: %s" % (self._cameratype, self._rotation)

    def __str__(self):
        return self.__unicode__()

def exif_fetch(filename):
    '''Open file, process EXIF data, return image orientation tag as string'''
    output = "None"
    try:
        f = open(filename, 'rb')
        tags = eso.exif.EXIF.process_file(f)
        output = str(tags['Image Orientation'])
    except KeyboardInterrupt:
        raise KeyboardInterrupt
    except:
        output = "Exception"
    finally:
        f.close()
    return output

def exif_tags(filename):
    '''Open file, return all EXIF data as object(?)'''
    f = open(filename, 'rb')
    return eso.exif.EXIF.process_file(f)

def original_dimensions(filename):
    '''Return the literal dimensions of the current image'''
    im = Image.open(filename)
    return im.size

def exif_translate(text):
    '''Convert EXIF rotation string tag to rotation angle in integer'''
    if text=="Rotated 90 CW":
        return 90
    if text=="Rotated 90 CCW":
        return 270
    if text=="Horizontal (normal)":
        return 0
    return None

def dimensions_translate(size):
    '''If the height of the file is greater than the width, lets guess
    that the file is rotated'''
    (width,height) = size;
    if (height>width):
        return 90
    return 0

def rotation_guess(er, dr):
    if er==90:
        return 90
    if er==270:
        return 270
    if dr==90:
        return 180 # means rotated, but we're not sure what direction
    return 0 # Means landscape

def old_main():
    #directory="/local/photos/jan04random"
    #pix=PictureSimple.objects.filter(directory=directory)
    pix=PictureSimple.objects.all()
    for pic in pix:
        if (pic.legacy):
            size = original_dimensions(
                "/local/img/" + pic.legacy.theme.directory + "/" + pic.legacy.filename + ".jpg")
        else:
            size = original_dimensions( pic.directory+"/"+pic.filename)
        er = exif_translate(exif_fetch(pic.directory+"/"+pic.filename))
        dr = dimensions_translate(size)
        pic.rotation=rotation_guess(er,dr)
        pic.save()
        print "Saved", pic.directory, pic.filename, rotation_guess(er,dr)

def main():
    directory1="/media/dev/photos/pdf03f"
    directory2="/media/dev/photos/alaska13"
    directory3="/media/dev/photos/devonjohn11"
    #pix=PictureSimple.objects.filter(directory=directory3)
    pix=PictureSimple.objects.all()
    for pic in pix:
        try:
            #print exif_fetch(pic.directory+"/"+pic.filename)
            print ExifReduced(exif_tags(pic.get_local_path()))
            er = exif_translate(exif_fetch(pic.get_local_path()))
            print "%s/%s as %s" % (pic.directory, pic.filename, er)
        except KeyboardInterrupt:
            print "Done loading: Interrupted by user"
            break
        #pic.rotation=rotation_guess(er,dr)
        #pic.save()
        #print "Saved", pic.directory, pic.filename, rotation_guess(er,dr)

if __name__ == '__main__':
    main()


import os
import glob
import itertools
import hashlib
from datetime import datetime
from django.conf import settings

import eso.exif.EXIF
from exo.models import Picture, Moment, PictureSimple

#path = '/media/dev/photos'
path = settings.NARTHEX_PHOTO_PATH

def exim_fetch(filename):
    """Read and reform file's EXIF timestamp as datetime string"""
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
    """Open file, compute md5 hash and return as ascii hex string"""
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
    """Recurse through the directory structure given the root directory"""
    for f in os.listdir(dirname):
        fullpath = os.path.join(dirname, f)
        if os.path.isfile(fullpath):
            if os.path.splitext(f)[1] in [".jpg",".JPG"]:
                print fullpath
                import_simple_picture(
                    f,dirname,datetime.fromtimestamp(os.stat(fullpath).st_mtime), md5_parse(fullpath))
        if os.path.isdir(fullpath):
            import_images(fullpath)

def import_simple_picture(filename, directory, stamp, file_hash):
    """Create a new picture object. Save filename, directory, and stamp information. Save. """
    ps=PictureSimple()
    ps.filename = filename
    ps.directory = directory
    ps.stamp = stamp
    ps.file_hash = file_hash
    ps.save()

def create_moment( mtime, ctime, exim):
    """This function is not used"""
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

def main():
    """Import images from the default path"""
    try:
        import_images(path)
    except KeyboardInterrupt:
        print "Done."
        exit

if __name__ == '__main__':
    main()


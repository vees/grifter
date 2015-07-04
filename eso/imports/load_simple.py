import os
import glob
import itertools
import hashlib
from datetime import datetime
from django.conf import settings

import eso.exif.EXIF
from exo.models import Picture, Moment, PictureSimple

class ImportRecursiveCount:
    def __init__(self, success, ignored, failure):
        print "Created IRC"
        self._import_success = success
        self._import_ignored = ignored
        self._import_failure = failure
        pass

    def __str__(self):
        return self.__unicode__()

    def __unicode__(self):
        return "Stats: %s %s %s" % (
            self._import_success, self._import_ignored, self._import_failure)

    def add(self, count_to_add):
        if isinstance(count_to_add, ImportRecursiveCount):
            self._import_success += count_to_add._import_success
            self._import_ignored += count_to_add._import_ignored
            self._import_failure += count_to_add._import_failure
        else:
            print "Failed to add object"
            pass

    def add_success(self):
        self._import_success += 1

    def add_ignored(self):
        self._import_ignored += 1
        #print self.__str__()

    def add_failure(self):
        self._import_failure += 1

basepath = settings.NARTHEX_PHOTO_PATH
import_debug = settings.NARTHEX_DEBUG_IMPORT

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

def import_images(reldirname):
    """Recurse through the directory structure given the root directory"""
    dirname = basepath + "/" + reldirname
    import_stats = ImportRecursiveCount(0,0,0)
    all_pictures = [basepath + '/' + ps.directory +'/'+ ps.filename
                    for ps in PictureSimple.objects.filter(directory=reldirname)]
    for f in os.listdir(dirname):
        fullpath = os.path.join(dirname, f)
        if os.path.isfile(fullpath):
            if os.path.splitext(f)[1] in [".jpg",".JPG"]:
                #match_count = all_pictures.filter(directory=dirname, filename=f).count()
                if fullpath not in all_pictures:
                    import_simple_picture(
                        f,reldirname,datetime.fromtimestamp(
                            os.stat(fullpath).st_mtime), md5_parse(fullpath))
                    if import_debug == True:
                        print "Import of " + fullpath
                    else:
                        import_stats.add_success()
                else:
                    if import_debug == True:
                        print "Cowardly not importing " + fullpath
                    else:
                        import_stats.add_ignored()
        if os.path.isdir(fullpath):
            subrecurse_stats = import_images(fullpath.replace(basepath + "/",''))
            print subrecurse_stats
            import_stats.add(subrecurse_stats)
            print import_stats
    return import_stats

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
        print import_images("")
    except KeyboardInterrupt:
        print "Done."
        exit

if __name__ == '__main__':
    main()


import os
import glob
import itertools
import hashlib
import ImportRecursiveCount

from datetime import datetime
from django.conf import settings
from exo.models import Picture, Moment, PictureSimple

basepath = settings.NARTHEX_PHOTO_PATH
import_debug = settings.NARTHEX_DEBUG_IMPORT

def hash_parse(filename):
    """Open file, compute md5 and sha2 hash and return as tuple"""
    try:
        f = open(filename, 'rb')
        content = f.read()
        md5hash = hashlib.md5(content).hexdigest()
        sha2hash = hashlib.sha256(content).hexdigest()
        return (md5hash,sha2hash)
    except ValueError:
        return 'No hash'
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

def sha2_parse(filename):
    """Open file, compute sha2 hash and return as ascii hex string"""
    try:
        f = open(filename, 'rb')
        content = f.read()
        sha2hash = hashlib.sha2(content).hexdigest()
        return sha2hash
    except ValueError:
        return 'No hash'
    finally:
        f.close()

def get_stat_hash(filename):
    """
    Some possible examples of use:
    >>> statinfo = os.stat('cels.html')
    posix.stat_result(st_mode=33204, st_ino=3707358L, st_dev=25L, st_nlink=1, st_uid=1000, st_gid=1000, st_size=163723L, st_atime=1422453686, st_mtime=1374702262, st_ctime=1374702262)
    >>> dir(statinfo)
    ['__add__', '__class__', '__contains__', '__delattr__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getitem__', '__getslice__', '__gt__', '__hash__', '__init__', '__le__', '__len__', '__lt__', '__mul__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__rmul__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', 'n_fields', 'n_sequence_fields', 'n_unnamed_fields', 'st_atime', 'st_blksize', 'st_blocks', 'st_ctime', 'st_dev', 'st_gid', 'st_ino', 'st_mode', 'st_mtime', 'st_nlink', 'st_rdev', 'st_size', 'st_uid']
    >>> print statinfo.st_mtime
    1374702262.18
    >>> print(datetime.datetime.fromtimestamp(os.stat('cels.html').st_mtime).strftime('%Y-%m-%d %H:%M:%S'))
    2013-07-24 17:44:22
    >>> int (statinfo.st_mtime)
    1374702262
    """
    statinfo = os.stat(filename)
    return statinfo.__hash__()

def get_hostname():
    import socket
    return socket.gethostname()

def files_under_dir(dirname):
    # Great example from http://stackoverflow.com/a/2186565/682915
    matches = []
    # Tuple is returned here, we just ignore dirnames because os.walk 
    # is following those on its own
    for root, dirnames, filenames in os.walk(dirname):
        for filename in filenames:
            matches.append(os.path.join(root, filename))
    return matches

def files_under_dir_2(dirname):
    """
    dirname is always the base_directory
    """
    # Great example from http://stackoverflow.com/a/2186565/682915
    matches = []
    # Tuple is returned here, we just ignore dirnames because os.walk 
    # is following those on its own
    for root, dirnames, filenames in os.walk(dirname):
        for filename in filenames:
            matches.append([root,filename])
    compare_list = [[dirname,os.path.relpath(root,dirname),filename,get_stat_hash(os.path.join(root,filename))] 
        for root,filename in matches]
    return compare_list
    

def files_and_stat(files):
    return [get_stat_hash(filename) for filename in files]

def import_masterfiles(reldirname):
    pass

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

def main():
    """Import images from the default path"""
    try:
        print import_images("")
    except KeyboardInterrupt:
        print "Done."
        exit

if __name__ == '__main__':
    main()

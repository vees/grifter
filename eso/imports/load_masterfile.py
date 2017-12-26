#!/usr/bin/env python
# -*- coding: ascii -*-

"""
"""

import os
import glob
import datetime
import itertools
import hashlib
from . import ImportRecursiveCount

from datetime import datetime
from django.conf import settings

basepath = settings.NARTHEX_PHOTO_PATH
import_debug = settings.NARTHEX_DEBUG_IMPORT

def hash_parse(filename):
    """Open file, compute md5 and sha2 hash and return as tuple"""
    try:
        print(filename)
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
    stats_total = 0
    stats_ignored = 0
    stats_updated = 0
    stats_inserted = 0
    try:
        for root, dirnames, filenames in os.walk(dirname):
            for filename in filenames:
                matches.append([root,filename])
                stats_total = len(matches)
        compare_list = {os.path.join(os.path.relpath(root,dirname),filename):
            [dirname,os.path.relpath(root,dirname),filename,get_stat_hash(os.path.join(root,filename))]
            for root,filename in matches}
        mfiles = MasterFile.objects.filter(base_directory=dirname)
        for mfile in mfiles:
            #print "Evaluating %s %s" % (mfile.filename, mfile.stat_hash)
            mfilepath=os.path.join(mfile.directory,mfile.filename)
            mfullfilepath=os.path.join(dirname,mfilepath)
            if mfilepath in compare_list:
                #print "Found file in db"
                if mfile.stat_hash == compare_list[mfilepath][3]:
                    #print "and hash already matches, so do nothing"
                    stats_ignored+=1
                else:
                    #print "and hash doesn't match, so update info"
                    oldstathash = mfile.stat_hash
                    md5, sha2 = hash_parse(mfullfilepath)
                    stat_hash = get_stat_hash(mfullfilepath)
                    mfile.hash_md5 = md5
                    mfile.hash_sha2 = sha2
                    mfile.stat_hash = stat_hash
                    mfile.updated = datetime.now()
                    mfile.save()
                    print("Updated %s from %s to %s" % (mfile.filename, oldstathash, stat_hash))
                    stats_updated+=1
                del compare_list[mfilepath]
            else:
                print("File not in db so I need to add it")

        for cfilekey in list(compare_list.keys()):
            cfile = compare_list[cfilekey]
            cfilepath = os.path.join(cfile[0],cfile[1],cfile[2])
            mfiles=MasterFile.objects.filter(base_directory=dirname)\
                .filter(directory=cfile[1]).filter(filename=cfile[2])
            md5, sha2 = hash_parse(cfilepath)
            stat_hash = get_stat_hash(cfilepath)
            if mfiles.count() == 0:
                m=MasterFile()
                m.filename = cfile[2]
                m.server = get_hostname()
                m.volume = "sda1"
                m.base_directory=dirname
                m.stat_hash = stat_hash
                m.directory = cfile[1]
                m.hash_md5 = md5
                m.hash_sha2 = sha2
                m.updated = datetime.now()
                m.save()
                stats_inserted+=1
        #return compare_list
    except KeyboardInterrupt:
        print("Keyboard interrupt recorded")
        pass
    finally:
        print("%s walked %s ignored, %s updated, %s inserted" % \
            (stats_total, stats_ignored, stats_updated, stats_inserted))

def files_and_stat(files):
    return [get_stat_hash(filename) for filename in files]

def report_duplicates():
	"""
	To remove duplicates we evaluate the directories and remove dups from
	the directory that contains the fewest files
	"""
	from exo.models import MasterFile
	from django.db.models import Count
	duplicates = MasterFile.objects.values('hash_sha2').annotate(filecopies=Count("id")).filter(filecopies__gt=1)
	dupcount = len(duplicates)
	print("Found %s duplicates" % dupcount)
	dircount = {}
	for duplicate in duplicates:
		for info in [[m.filename,m.directory,m.hash_md5[:8],m.hash_sha2[:8]] for m in MasterFile.objects.filter(hash_sha2=duplicate["hash_sha2"])]:
			if m.directory in dircount:
				dircount[m.directory]+=1
			else:
				dircount[m.directory]=1
			print(info)
	for dk in list(dircount.keys()):
		print("%s: %s" % (dk, dircount[dk]))
	return dupcount

def report_duplicates_2():
	"""
	To remove duplicates we evaluate the directories and remove dups from
	the directory that contains the fewest files
	"""
	from exo.models import MasterFile
	from django.db.models import Count
	from eso.imports import DuplicateCounter
	duplicates = MasterFile.objects.values('hash_sha2').annotate(filecopies=Count("id")).filter(filecopies__gt=1)
	dc=DuplicateCounter.DuplicateCounter()
	for duplicate in duplicates:
		dc.add([m.directory for m in MasterFile.objects.filter(hash_sha2=duplicate["hash_sha2"])])
	dc.results()
	return None

def main():
    """Import images from the default path"""
    try:
        print(import_images(""))
    except KeyboardInterrupt:
        print("Done.")
        exit

if __name__ == '__main__':
    main()

# -*- coding: utf-8 -*-
"""
Import from local directory
"""

import os
import socket
from eso.imports import walk
from exo.models import ContentInstance, ContentContainer, ContentSignature
from exo.models import ContentKey
import eso.base32.randspace

def walk_card(path):
    from datetime import datetime
    start = datetime.now()
    walked = walk.file_dir_stat_size(path)
    end = datetime.now()
    duration = end-start
    print(duration)
    return walked

def data_load(walked, server, drive, path):
    # Keep track of files walked in n and report every 1000 with the modulo
    n=0
    c, created = ContentContainer.objects.get_or_create(
        server=server, drive=drive, path=path)
    for walkunit in walked:
        n+=1
        if (n % 1000 == 0):
            print(n)
        cs, createds = ContentSignature.objects.get_or_create(
            md5=walkunit[6], sha2=walkunit[7],
            content_size=walkunit[5])
        ci, createdi = ContentInstance.objects.get_or_create(
            filename = walkunit[2],
            content_container = c,
            relpath=walkunit[3],
            stat_hash=walkunit[4],
            content_signature=cs)
        print("Sig",createds,"Instance", createdi,walkunit[2])

def grant_keys():
    cs = ContentSignature.objects.filter(content_key=None)
    for sig in cs:
        try:
            duplicate_key=1
            while duplicate_key>0:
                newkey=eso.base32.randspace.randid()
                duplicate_key=ContentKey.objects.filter(key=newkey).count()
            ck = ContentKey.objects.create(key=newkey)
            sig.content_key=ck
            sig.save()
        except django.db.utils.IntegrityError:
            print("duplicate key %s for sig id %s" % (newkey, cs.id))
            continue

def load_dir(path):
    servername = socket.gethostname()
    walked=walk_card(path)
    data_load(walked, servername, servername, path)
    grant_keys()

import os
from datetime import datetime

def get_stat_hash(filename):
    statinfo = os.stat(filename)
    return statinfo.__hash__()

def files_under_dir(dirname):
    #Great example from http://stackoverflow.com/a/2186565/682915
    matches = []
    for root, dirnames, filenames in os.walk(dirname):
        for filename in filenames:
            matches.append(os.path.join(root, filename))
    return matches

def files_and_stat(files):
    return [(filename,get_stat_hash(filename)) for filename in files]

start = datetime.now()
foo = files_and_stat(files_under_dir("/media/dev/photos"))
end = datetime.now()
print end-start
print len(foo)

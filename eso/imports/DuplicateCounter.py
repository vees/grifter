#!/usr/bin/env python
# -*- coding: ascii -*-

"""Find duplicates already residing on the system
"""

class DuplicateCounter:
    def __init__(self):
        self._dirdict = {}
        pass
        
    def add(self, shareddirlist):
        for dir1 in shareddirlist:
            if dir1 not in self._dirdict:
                self._dirdict[dir1]={}
            for dir2 in shareddirlist:
                if dir2 not in self._dirdict[dir1]:
                    self._dirdict[dir1][dir2]=1
                else:
                    self._dirdict[dir1][dir2]+=1
            self._dirdict[dir1][dir1]-=1

    def results(self):
        for dir1 in list(self._dirdict.keys()):
            # http://stackoverflow.com/q/8717395/682915
            shares = ', '.join(['%s (%s)' % (key, value) for (key, value) in list(self._dirdict[dir1].items()) if value != 0])
            print("%s shares files with: %s" % (dir1, shares))


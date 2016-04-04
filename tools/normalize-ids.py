#!/usr/bin/python

import os,sys,json,re
from LRR.utils import Utils

utils = Utils()

jurisdiction = sys.argv[1]



for dirpath,dirnames,filenames in os.walk("data/courts/%s" % jurisdiction):
    indexPath = os.path.join(dirpath,"index.txt")
    if not os.path.exists(indexPath):
        print "Oops: %s" % indexPath
        sys.exit()

    fh = open(indexPath)
    lines = []
    template = None
    firstContent = False
    isCourt = False
    while 1:
        line = fh.readline()
        if not line: break
        if line.find(':category-id:') > -1: continue
        if line.find(':court-id:') > -1: continue
        line = line.rstrip()
        if not firstContent:
            if not line: continue
            firstContent = True
        if line.startswith('.. category:: '):
            template = '   :category-id: %s'
        elif line.startswith('.. court:: '):
            isCourt = True
            template = '   :court-id: %s'
        lines.append(line)
    fh.close()

    if not template:
        print "Ouch: %s" % indexPath
        sys.exit()

    if isCourt:
        id = utils.joinUrn(dirpath.split("/")[2:], True)
    else:
        id = ":".join(dirpath.split("/")[2:])
    lines = lines[0:1] + [template % id] + lines[1:]
    txt = "\n".join(lines) + "\n"

    sys.stdout.write(".");\
    sys.stdout.flush()
    open(indexPath, "w+").write(txt)

#!/usr/bin/python

import os,sys,json,re

for dirpath,dirnames,filenames in os.walk("data/courts/us"):
    indexPath = os.path.join(dirpath,"index.txt")
    if not os.path.exists(indexPath):
        print "Oops: %s" % indexPath
        sys.exit()

    fh = open(indexPath)
    lines = []
    template = None
    firstContent = False
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
            template = '   :court-id: %s'
        lines.append(line)
    fh.close()

    if not template:
        print "Ouch: %s" % indexPath
        sys.exit()

    id = ';'.join(dirpath.split("/")[2:])
    lines = lines[0:1] + [template % id] + lines[1:]
    txt = "\n".join(lines) + "\n"

    print txt
    
    #open(indexPath, "w+").write(txt)

#!/usr/bin/python

import sys,os,json

obj = json.loads(open("courts-final.json").read())

stub = "data/courts"

for key in obj.keys():
    courtID = obj[key][0]
    courtName = obj[key][1]
    pth = os.path.join(stub, courtID.replace(";", "/"), "index.txt")
    fh = open(pth)
    txt = ''
    while 1:
        line = fh.readline()
        if not line: break
        if line.startswith(".. court::"):
            line = ".. court:: %s\n" % courtName
        txt += line
    fh.close()
    fh = open(pth, "w+").write(txt)

    

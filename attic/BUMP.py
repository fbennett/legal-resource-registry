#!/usr/bin/python

import os,shutil

allthings = {}

rootpath = os.path.abspath(".")

def listup(arg, dirname, fnames):
    courtpath = os.path.join(rootpath,dirname,"index.txt")
    dirlst = dirname.split("/")
    if os.path.exists(courtpath) and len(dirlst) > 4 and dirlst[-2] != "federal" and dirlst[2] == "us":
        arg[dirname] = True

os.path.walk("data/reporters", listup, allthings)

for path in allthings.keys():
    fr = path
    tolst = path.split("/")
    tolst.pop(-2)
    to = "/".join(tolst)
    shutil.move(fr,to)

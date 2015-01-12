#!/usr/bin/python

import os

for stateCode in os.listdir("data/courts/us/state"):
    if len(stateCode) > 2: continue
    txt = open("data/courts/us/state/%s/index.txt" % stateCode).read()
    lst = txt.split("\n")
    lst = lst[0:2] + ['   :set-form:'] + lst[2:]
    txt = "\n".join(lst)
    open("data/courts/us/state/%s/index.txt" % stateCode, "w+").write(txt)

        

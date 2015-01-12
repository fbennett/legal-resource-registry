#!/usr/bin/python

import os,sys,json

obj = json.loads(open("HEADINGS.json").read())

for key in obj:
    print key
    obj[key] = []

open("HEADINGS.json","w+").write(json.dumps(obj,indent=2))

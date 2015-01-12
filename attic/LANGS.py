#!/usr/bin/python

import json,os,re

langs = json.loads(open("LANGS.json").read())

lst = []

for key in langs:
    str = langs[key]
    str = re.sub("\s*\(.*","",str)
    str = "%s (%s)" % (str,key)
    lst.append(str)

lst.sort()
    
open("LANGS_OUT.json","w+").write(json.dumps(lst,indent=2))

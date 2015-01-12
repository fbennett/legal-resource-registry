#!/usr/bin/python

import sys,os,json

obj = json.loads(open("reporters-db.json").read())

def sortme(a,b):
    if a["name"] > b["name"]:
        return 1
    elif a["name"] < b["name"]:
        return -1
    else:
        return 0

for key in obj.keys():
    bundle = obj[key]
    bundle.sort(sortme)
    for series in bundle:
        series["mlz_jurisdiction"].sort()

open("reporters-db-new.json","w+").write(json.dumps(obj,indent=2,sort_keys=True))

#!/usr/bin/python

import json

obj = json.loads(open("court-map.json").read())

newobj = {}

for key in obj.keys():
    urn = ";".join(obj[key].split(";")[0:-1])
    newobj[urn] = True

newlst = []
for key in newobj.keys():
    newlst.append(key)

open("new-places.json", "w+").write(json.dumps(newobj, sort_keys=True, indent=2))

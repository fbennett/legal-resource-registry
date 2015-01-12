#!/usr/bin/python

import json,sys

old = json.loads(open("reporters.js").read())

new = json.loads(open("reporters-db.json").read())

for okey in old.keys():
    if not new.has_key(okey):
        print "Dropped reporter key: %s" % okey
        sys.exit()

for nkey in new.keys():
    if not old.has_key(nkey):
        print "New reporter key: %s" % nkey

for okey in old.keys():
    newBundle = new[okey]
    oldBundle = old[okey]
    if len(newBundle) != len(oldBundle):
        print "Change in length for %s" % okey
        sys.exit()
    if len(newBundle) > 1:
        for i in range(0,len(newBundle),1):
            if oldBundle[i]["name"] != newBundle[i]["name"]:
                print "DISCREPANCY: %s" % okey
                print "  Old: %s" % oldBundle[i]["name"]
                print "  New: %s" % newBundle[i]["name"]
        #sys.exit()
    for i in range(0,len(newBundle)):
        newBundle[i]["mlz_jurisdiction"] = oldBundle[i]["mlz_jurisdiction"]

open("reporters-db-new.json","w+").write(json.dumps(new,indent=2,sort_keys=True))

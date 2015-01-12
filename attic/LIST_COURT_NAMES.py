#!/usr/bin/python

import sys,os,json,re

def sortByLength(a,b):
    if len(a) > len (b):
        return 1
    elif len(a) < len(b):
        return -1
    else:
        return 0

names = json.loads(open("resource/courts.json").read())

states = json.loads(open("attic/STATES.json").read())
lstates = []
for key in states.keys():
    lstates.append(states[key])
lstates.append("United States")
lstates.append("U.S.")
lstates.sort(sortByLength)
rxstates = re.compile("(?:" + "|".join(lstates) + ")")

obj = {}
for name in names:
    full = name["fields"]["full_name"]
    full = full.split(",")[0]
    nostate = " ".join(re.split(rxstates,full)).strip()
    #print full
    #print "  %d" % len(re.split(rxstates,full))
    nostate = re.sub("\s+of\s*(\.|the\s*)*$", "", nostate)
    notstate = nostate.strip()
    obj[name["pk"]] = nostate

open("newcourts.json", "w+").write(json.dumps(obj, sort_keys=True, indent=2))

#!/usr/bin/python

import sys,json, re

obj = {}

placesMap = json.loads(open("map-places.json").read())

print "=== PLACES ==="
oldPlaces = json.loads(open("old-places.json").read())
placeKeys = json.loads(open("key-places.json").read())
for key in oldPlaces:
    if placesMap.has_key(key):
        key = placesMap[key]
    if not placeKeys.has_key(key):
        print "Oops: %s -- %s" % (key, oldPlaces[key])

print "=== COURTS ==="
oldCourts = json.loads(open("old-courts.json").read())
courtKeys = json.loads(open("key-courts.json").read())
circuitsByCourt = {}
for key in courtKeys:
    if not key.startswith("us;c"): continue
    m = re.match("^us;(c[0-9]{1,2});([a-z]{2})(?:[\-.].*)$", key)
    if m:
        if not circuitsByCourt.has_key(m.group(2)):
            circuitsByCourt[m.group(2)] = m.group(1)

courtsMap = {}

for key in oldCourts:

    compass = {
        "eastern": "ed",
        "western": "wd",
        "southern": "sd",
        "northern": "nd",
        "middle": "md",
        "central": "cd",
        None: "d"
        }

    circuits = {
        "1-cir": "c1",
        "2-cir": "c2",
        "3-cir": "c3",
        "4-cir": "c4",
        "5-cir": "c5",
        "6-cir": "c6",
        "7-cir": "c7",
        "8-cir": "c8",
        "9-cir": "c9",
        "10-cir": "c10",
        "11-cir": "c11"
        }

    origKey = key

    m = re.match("^us;federal;([a-z]{2})[\.]{0,1}(eastern|middle|central|southern|northern|western)*[\-]{0,1}(bankr)*$", key)
    mm = re.match("^us;federal;([0-9]{1,2}-cir)[\-]*(bankr)*$", key)
    if m:
        state = m.group(1)
        district = compass[m.group(2)]
        bankruptcy = m.group(3)
        key = "us;" + circuitsByCourt[state] + ";" + state + "." + district
        if bankruptcy:
            key = key + ";bankruptcy.court"
        else:
            key = key + ";district.court"
    elif mm:
        key = "us;" + circuits[mm.group(1)]
        if mm.group(2):
            key = key + ";bankruptcy.appellate.panel"
        else:
            key = key + ";court.appeals"
            
    if key == "us;federal;supreme.court":
        key = "us;supreme.court"
    if key == "un;icj":
        key = "un.int;international.court.justice"
    if key == "un.org;icj":
        key = "un.int;international.court.justice"
    if key == "coe.int;commission.on.human.rights":
        key = "coe.int;commission.human.rights"

    if not courtKeys.has_key(key):
        print "Oops: %s -- %s" % (key, oldCourts[origKey])
        pass
    courtsMap[origKey] = key
    
open("map-courts.json", "w+").write(json.dumps(courtsMap, sort_keys=True, indent=2))

#!/usr/bin/python

import json,os,sys,re

states = json.loads(open("STATES.json").read())

districts = json.loads(open("DISTRICTS.json").read())

#circuits = json.loads(open("CIRCUITS.json").read())

for stateCode in os.listdir("data/courts/us/federal/state"):
    if len(stateCode) > 2: continue
    stateName = states[stateCode]
    for districtCode in os.listdir("data/courts/us/federal/state/%s" % stateCode):
        if len(districtCode) > 1: continue
        districtName = districts[districtCode]
        print districtCode
        fh = open("data/courts/us/federal/state/%s/%s/index.txt" % (stateCode,districtCode), "w+")
        fh.write(".. category:: %s\n   :category-id: us;federal;state;%s;%s" % (districtName, stateCode, districtCode))
        fh.close()

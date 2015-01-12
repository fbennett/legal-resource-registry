#!/usr/bin/python

import json, sys, os, re

obj = json.loads(open("lexadin-deriv/11-countrycode-keyed.json").read())  

def sortByName(a,b):
    if a["countryName"] > b["countryName"]:
        return 1
    elif a["countryName"] < b["countryName"]:
        return -1
    else:
        return 0

lst = []
for key in obj.keys():
    lst.append({
        "countryName": obj[key]["country-name"],
        "url": "proofs-by-excel/%s.xlsx" % key
        })

lst.sort(sortByName) 

for item in lst:
    print "   .. bubble-link:: %s\n      :url: %s\n" % (item["countryName"], item["url"])

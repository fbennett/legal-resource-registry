#!/usr/bin/python

import json,re

newObj = {}

keyedCountryJson = json.loads(open("attic/ALL-COURTS.json").read())

localKeys = {}

keys = {}
for key in keyedCountryJson.keys():
    country = keyedCountryJson[key]["country-name"]
    keys[country] = key
    localKeys[country] = {}
    for kkey in keyedCountryJson[key]["courts"].keys():
        courtObj = keyedCountryJson[key]["courts"][kkey]
        #newCourtKey = courtObj["court-id"]
        #newCourtObj = {
        #    "en": courtObj["name"],
        #    }
        #if courtObj.has_key("url"):
        #    newCourtObj["url"] = courtObj["url"]
        if courtObj.has_key("local"):
            if re.match("[^ a-zA-Z]", courtObj["local"]):
                #print "%s: %s --> %s" % (country,courtObj["en"],courtObj["local"])
                #print "%s: %s" % (country,courtObj["en"])
                localKeys[country][courtObj["en"]] = courtObj["local"]
                #newCourtObj["local"] = courtObj["local"]
                                   
dataCountryJson =  json.loads(open("lexadin-deriv/10-countryname-keyed.json").read())

for country in dataCountryJson.keys():
    if not keys.has_key(country):
        print country
    
    for courtKey in localKeys[country].keys():
        # Iterate over court categories
        # Iterate over courts in list
        # If key not found, say so.
        hasKey = False
        for category in dataCountryJson[country].keys():
            courtLst = dataCountryJson[country][category]
            for court in courtLst:
                if localKeys[country].has_key(court["name"]):
                    hasKey = True
        if not hasKey:
            print "No match found: %s / %s" % (country, court["name"])
            print "  %s" % courtKey

        ## Now that this is clearing, we can transform the
        ## objects in dataCountryJson, stirring in the translated text.

    newObj[keys[country]] = {}
    newObj[keys[country]]["country-name"] = country
    newObj[keys[country]]["courts"] = {}

    # Do ...
    for category in dataCountryJson[country].keys():
        newObj[keys[country]]["courts"][category] = {}
        courtLst = dataCountryJson[country][category]
        newCourtObj = {}
        for courtIndex in range(0,len(courtLst),1):
            court = courtLst[courtIndex]
            courtObj = {}
            courtObj["en"] = court["name"]
            if court.has_key("url"):
                courtObj["url"] = court["url"]
            if localKeys[country].has_key(court["name"]):
                courtObj["local"] = localKeys[country][court["name"]]
            newObj[keys[country]]["courts"][category][court["court-id"]] = courtObj

open("lexadin-deriv/11-countrycode-keyed.json","w+").write(json.dumps(newObj,sort_keys=True,indent=2))

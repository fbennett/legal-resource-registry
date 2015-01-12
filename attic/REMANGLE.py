#!/usr/bin/python

import sys,os,json,re
from unidecode import unidecode

newObj = {}
oldObj = json.loads(open("lexadin-deriv/00-category-keyed.json").read())

particles = {}
totalPops = 0

for category in oldObj:
    if category == "International Courts": continue
    if category == "Judiciary (general)": continue
    if category == "Jurisprudence (Case Law)": continue
    if category == "Minor Courts Justices of the Peace": continue
    #if category == "Administrative Courts (First Instance)": continue
    #if category == "Federal Courts of First Instance": continue
    #if category == "Federal District Courts": continue
    #if category == "Federal District Courts of First Instance": continue
    #if category == "Federal Territorial Courts": continue
    #if category == "First Instance Courts": continue
    #if category == "Labor Courts": continue
    #if category == "Regional Arbitration Courts": continue
    #if category == "Regional courts": continue
    #if category == "Religious Courts": continue

    for oldCountryObj in oldObj[category]:
        country = oldCountryObj["country"]
        if not newObj.has_key(country):
            newObj[country] = {}
        if not newObj[country].has_key(category):
            newObj[country][category] = []
        courtNames = []
        for courtObj in oldCountryObj["courts"]:
            if courtObj["name"] == "Royal Court Rules": continue
            if courtObj["name"] == "Arbitration Court Moscow": continue
            if courtObj["name"] == "Lands Court": continue
            #courtNames.append(re.sub("\s+\([^)]{1,3}\)$","XXX",courtObj["name"]))
            courtNames.append(courtObj["name"])
        for i in range(len(courtNames)-1,-1,-1):
            chop = False
            for j in range(len(courtNames)-1,-1,-1):
                if j == i:
                    continue
                if courtNames[j] == "The Supreme Court of Nahchivan Autonomous Republic": continue
                if courtNames[j] == "Corte d'Assise d'Appello": continue
                if courtNames[j] == courtNames[i]:

                    # XXX We have duplicate names. Save an element that
                    # XXX has a URL if possible.
                    # XXX Tricky to do, since [j] could precede [i], and
                    # XXX removing it would damage the list.
                    if j > i:
                        if oldCountryObj["courts"][j].has_key("url"):
                            chop = True
                            break
                        elif not oldCountryObj["courts"][j].has_key("url") and not oldCountryObj["courts"][i].has_key("url"):
                            chop = True
                            break
                if courtNames[j].startswith(courtNames[i] + " "):
                    #print "Popping: \"%s\" because \"%s\"" % (courtNames[i], courtNames[j])
                    chop = True
                    break
            if chop:
                totalPops += 1
                courtNames.pop(i)
                continue
            
            # XXX Actually, the stuff below needs to go here, so that the
            # XXX result can be added to the court object as "court-id".
            m = re.match("^(.*)(?:\s+(\(.*))*", unidecode(oldCountryObj["courts"][i]["name"]).lower())
            pre = m.group(1)
            if m.group(2):
                post = m.group(2)
            else:
                post = ""
            pre = re.sub("[-/&\.,:\s,\'()]+"," ", pre)
            post = re.sub("[-/&\.,:\s,\'()]+"," ", post)
            pre = pre.split()
            post = post.split()
            prepositions = {}
            prepositions["a"] = True
            prepositions["the"] = True
            prepositions["of"] = True
            prepositions["for"] = True
            prepositions["y"] = True
            for j in range(len(pre)-1,-1,-1):
                pre[j] = re.sub("^([0-9]+)[a-z]+","\\1",pre[j])
                if prepositions.has_key(pre[j]):
                    pre.pop(j)
            courtID = [".".join(pre)]
            if post:
                courtID.append(".".join(post))
            courtID = ".".join(courtID)
            oldCountryObj["courts"][i]["court-id"] = courtID

            newObj[country][category].append(oldCountryObj["courts"][i])

            # XXX Need a smarter function for this.
            # XXX Remove obvious prepositions and articles (English only).
            # XXX Simplify numbers.
            # XXX Maybe move aside trailing parentheticals before doing the replacements?

            # XXX After that, we need to add country keys, then map in native-script names from Wikipedia
            # XXX data. Then we should be ready to go.

            # XXX Most of this can be marked as held in reserve in the repo;
            # XXX only confirmed domains should be mapped through to the MLZ
            # XXX jurisdictions object (beyond the country code, which is already
            # XXX in there.
 
            #print re.sub("[,\'()]","",re.sub("[-/,:\s]+","-",unidecode(oldCountryObj["courts"][i]["name"]).lower()))


print totalPops

open("lexadin-deriv/10-countryname-keyed.json","w+").write(json.dumps(newObj,sort_keys=True,indent=2))

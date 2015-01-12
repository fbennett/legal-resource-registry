#!/usr/bin/python

import json,re,sys,os

scriptpath = os.path.dirname(sys.argv[0])
rootpath = os.path.join(scriptpath, os.path.pardir)
rootpath = os.path.abspath(rootpath)
LRRpath = os.path.join(rootpath, "tools", "LRR")
LRRpath = os.path.abspath(LRRpath)
sys.path.append(LRRpath)

from excelExport import LRRWorkbook

obj = json.loads(open(os.path.join(rootpath,"lexadin-deriv/11-countrycode-keyed.json")).read())

categories = {}

def hasDuplicates(obj, countryKey, category):
    categoryNames = {}
    for courtKey in obj[countryKey]["courts"][category].keys():
        courtName = obj[countryKey]["courts"][category][courtKey]["en"]
        courtName = re.sub("(.*)\(.*","\\1",courtName)
        courtName = courtName.strip()
        if not categoryNames.has_key(courtName):
            categoryNames[courtName] = True
            obj[countryKey]["courts"][category][courtKey]["en"] = courtName
        else:
            print "Duplicate: %s : %s : %s" % (obj[countryKey]["country-name"],category,courtName)
            return True
    return False
    

for countryKey in obj.keys():
    # popCats
    popCats = {}
    keys = obj[countryKey]["courts"].keys()
    for pos in range(len(keys)-1,-1,-1):
        category = keys[pos]
        count = 0
        for court in obj[countryKey]["courts"][category].keys():
            count += 1
        # Strip parentheticals on courts in category if it does not create duplicates
        if hasDuplicates(obj, countryKey, category):
            sys.exit()
            
        if count == 1 or category == "Other Courts":
            skipCategory = False
            kkeys  = obj[countryKey]["courts"][category].keys()
            for ppos in range(len(kkeys)-1,-1,-1):
                courtKey = kkeys[ppos]
                courtObj = obj[countryKey]["courts"][category][courtKey]
                if courtObj["en"].endswith("s") and count == 1:
                    if category == "Court of Audit": continue
                    if courtObj["en"].find("Marshal") > -1: continue
                    if courtObj["en"].find("Cour de Comptes") > -1: continue
                    if courtObj["en"].find("The Constitutional Court of the Republic of Belarus") > -1: continue
                    if courtObj["en"].find("The Court of Accounts") > -1: continue
                    if courtObj["en"].find("Tribunal Superior de Cuentas") > -1: continue
                    if courtObj["en"].find("Corte Suprema de Justicia Honduras") > -1: continue
                    if courtObj["en"].find("Board of Grievances") > -1: continue
                    if courtObj["en"].find("Supreme Court of Mauritius") > -1: continue
                    if courtObj["en"].find("Maldives") > -1: continue
                    if courtObj["en"].find("Tribunal Supremo de Elecciones") > -1: continue
                    if courtObj["en"].find("Turkish Court of Accounts") > -1: continue
                    if courtObj["en"].find("Court of Appeals") > -1: continue
                    if courtObj["en"].find("Tribunal de Contas") > -1: continue

                    #print "PLURAL: %s: %s -- %s" % (countryKey,category,courtObj["en"])
                    # XXX TEMPORARY - RESTORE
                    obj[countryKey]["courts"].pop(category)
                    skipCategory = True
            if skipCategory:
                continue
            # Move "Other Courts" category and categories with a single court only to the top level
            if not obj[countryKey]["courts"].has_key("top"):
                obj[countryKey]["courts"]["top"] = {}
            for courtKey in obj[countryKey]["courts"][category].keys():
                obj[countryKey]["courts"]["top"][courtKey] = obj[countryKey]["courts"][category][courtKey]
                popCats[category] = True
            # ?? 
        if not categories.has_key(category):
            categories[category] = {}
        categories[category][countryKey + ": " + obj[countryKey]["country-name"]] = True

    for category in popCats.keys():
        # XXX TEMPORARY - RESTORE
        obj[countryKey]["courts"].pop(category)
        pass

def sortCategories(a,b):
    if a != b and b == "top":
        return 1
    elif a != b and a == "top":
        return -1
    elif a > b:
        return 1
    elif a < b:
        return -1
    else:
        return 0

def sortCourtInfo(a,b):
    if a["en"] > b["en"]:
        return 1
    elif a["en"] < b["en"]:
        return -1
    else:
        return 0

for countryCode in obj.keys():
    if True:
        countryName = obj[countryCode]["country-name"]
        workbook = LRRWorkbook(os.path.join(rootpath, "public/proofs-by-excel/%s" % countryCode), countryCode, countryName)
        print countryName
        categoryLst = []
        for categoryKey in obj[countryCode]["courts"].keys():
            categoryLst.append(categoryKey)
        categoryLst.sort(sortCategories)
        for categoryKey in categoryLst:
            print "  " + categoryKey
            lst = []
            for court in obj[countryCode]["courts"][categoryKey].keys():
                lst.append(obj[countryCode]["courts"][categoryKey][court])
            lst.sort(sortCourtInfo)
            workbook.write_heading(categoryKey)
            for i in range(0, len(lst), 1):
                courtInfo = lst[i]
                print "    " + courtInfo["en"]
                if courtInfo.has_key("url"):
                    url = courtInfo["url"]
                else:
                    url = ''
                if i == len(lst)-1:
                    lastNode = True
                else:
                    lastNode = False
                if courtInfo.has_key("local"):
                    localScript = courtInfo["local"]
                else:
                    localScript = courtInfo["en"]
                if courtInfo.has_key("roman"):
                    romanScript = courtInfo["roman"]
                else:
                    romanScript = ''
                workbook.write_datarow(localScript, romanScript, courtInfo["en"], '', url)
        workbook.close()

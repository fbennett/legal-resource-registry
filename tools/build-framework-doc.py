#!/usr/bin/python

import sys,os,os.path,re,json

scriptpath = os.path.dirname(sys.argv[0])
rootpath = os.path.join(scriptpath,os.path.pardir)
rootpath = os.path.abspath(rootpath)

datasrcpath = os.path.join(rootpath,'resource','reporters.js')
datasrc = open(datasrcpath)
datasrc.seek(15)

data = json.load(datasrc)

jurisdictions = {}

str = '''.. fields::
   :casename: required
   :jurisdiction: required
   :date-published: default
   :volume: default
   :reporter: default
   :page: default
   :decision-number: auxiliary
   :date-decided: auxiliary
   :docket-number: auxiliary
   :court-place: optional

.. citation-group:: United States Courts
'''

def mkCourt(key):
    ords = ["First","Second","Third","Fourth","Fifth","Sixth","Seventh","Eighth","Ninth","Tenth","Eleventh"]
    tmpl = "United States Circuit Court of Appeals for the %s Circuit"
    keychain = {
        "us;federal;1-cir": tmpl % ords[0],
        "us;federal;2-cir": tmpl % ords[1],
        "us;federal;3-cir": tmpl % ords[2],
        "us;federal;4-cir": tmpl % ords[3],
        "us;federal;5-cir": tmpl % ords[4],
        "us;federal;6-cir": tmpl % ords[5],
        "us;federal;7-cir": tmpl % ords[6],
        "us;federal;8-cir": tmpl % ords[7],
        "us;federal;9-cir": tmpl % ords[8],
        "us;federal;10-cir": tmpl % ords[9],
        "us;federal;11-cir": tmpl % ords[10]
        }
    if keychain.has_key(key):
        return keychain[key]
    else:
        return key

for key in data:
    rptr = data[key]
    for obj in rptr:
        for jdct in obj["mlz_jurisdiction"]:
            if not jurisdictions.has_key(jdct):
                jurisdictions[jdct] = {}
                jurisdictions[jdct]["name"] = mkCourt(jdct)
                jurisdictions[jdct]["reporters"] = []
            for ekey in obj["editions"]:
                edn = obj["editions"][ekey]
                edition = {}
                edition["title"] = ekey
                if edn[0]["year"] == False:
                    edition["start"] = "present"
                else:
                    edition["start"] = "%d/%d/%d" % (edn[0]["year"],edn[0]["month"]+1,edn[0]["day"])
                if edn[1]["year"] == False:
                    edition["end"] = "present"
                else:
                    edition["end"] = "%d/%d/%d" % (edn[1]["year"],edn[1]["month"]+1,edn[1]["day"])
                edition["name"] = obj["name"]
                edition["series-abbreviation"] = ekey
                if obj["cite_type"] == "neutral":
                    edition["neutral"] = True
                else:
                    edition["neutral"] = False

                jurisdictions[jdct]["reporters"].append(edition)
    
def sortcourts (a,b):
    fedA = False
    fedB = False
    a = re.sub(";([0-9])-cir",";0\\1-cir",a)
    b = re.sub(";([0-9])-cir",";0\\1-cir",b)
    if a == "us" or a.startswith("us;federal"):
        fedA = True
    if b == "us" or b.startswith("us;federal"):
        fedB = True
    if fedA != fedB:
        if fedB:
            return 1
        else:
            return -1
    elif a > b:
        return 1
    elif a < b:
        return -1
    else:
        return 0

def sortreporters(a,b):
    if a["name"] > b["name"]:
        return 1
    elif a["name"] < b["name"]:
        return -1
    else:
        return 0

jkeys = []
for jkey in jurisdictions:
    jkeys.append(jkey)

jkeys.sort(sortcourts)
for jkey in jkeys:
    jurisdiction = jurisdictions[jkey]
    str += '\n.. court:: %s\n   :court-id: %s\n' % (jurisdictions[jkey]["name"],jkey)
    reporters = []
    for reporter in jurisdiction["reporters"]:
        reporters.append(reporter)
    reporters.sort(sortreporters)
    for reporter in reporters:
        #reporter = jurisdiction["reporters"][rkey]
        if reporter["neutral"]:
            neutral = "      :neutral:\n"
        else:
            neutral = ""
            
        str += '\n   .. reporter:: %s\n      :series-abbreviation: %s\n      :dates: %s-%s\n%s' % (reporter["name"],reporter["series-abbreviation"],reporter["start"],reporter["end"],neutral)

#print json.dumps(jurisdictions,indent=2,sort_keys=True)

print str

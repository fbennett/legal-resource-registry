#!/usr/bin/python

import sys,os,os.path,re,json

scriptpath = os.path.dirname(sys.argv[0])
rootpath = os.path.join(scriptpath,os.path.pardir)
rootpath = os.path.abspath(rootpath)

datasrcpath = os.path.join(rootpath,'resource','reporters.js')
datasrc = open(datasrcpath)
datasrc.seek(0)
data = json.load(datasrc)

statemapsrcpath = os.path.join(rootpath,'resource','state_jur_map.json')
state_jur_map = json.loads(open(statemapsrcpath).read())

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

# Actually, we should have a remapper that translates to the canonical MLZ IDs,
# and then an object that contains everything under the canonical IDs as key.
remap = {
    "us;federal;supreme.court": "us;federal;supreme.court",
    "us;federal;1-cir": "us;federal;court.appeals.1.circuit",
    "us;federal;2-cir": "us;federal;court.appeals.2.circuit",
    "us;federal;3-cir": "us;federal;court.appeals.3.circuit",
    "us;federal;4-cir": "us;federal;court.appeals.4.circuit",
    "us;federal;5-cir": "us;federal;court.appeals.5.circuit",
    "us;federal;6-cir": "us;federal;court.appeals.6.circuit",
    "us;federal;7-cir": "us;federal;court.appeals.7.circuit",
    "us;federal;8-cir": "us;federal;court.appeals.8.circuit",
    "us;federal;9-cir": "us;federal;court.appeals.9.circuit",
    "us;federal;10-cir": "us;federal;court.appeals.10.circuit",
    "us;federal;11-cir": "us;federal;court.appeals.11.circuit",
    "us;dc": "us;federal;district.columbia.court.appeals", 
    "us;pr": "us;federal;district.court.d.puerto.rico", 
    "us;am": "us;federal;high.court.american.samoa",
    "us;vi": "us;federal;district.court.virgin.islands",
    "us;mp": "us;federal;district.court.northern.mariana.islands",
    "us;gu": "us;federal;district.court.d.guam"
    }

# Hmm. The Federal courts of special jurisdiction all have the
# key "us" on reporters.js-side. There are twenty-five of them,
# so fixable.

keychain = {}
keychain.update(state_jur_map)
keychain["us;federal;court.customs.appeals"] = ["us;federal;court.customs.appeals","United States Court of Customs Appeals","http://en.wikipedia.org/wiki/United_States_Court_of_Customs_and_Patent_Appeals",None]
keychain["us;judicial.branch.navajo.nation"] = ["us;judicial.branch.navajo.nation","Judicial Branch of the Navajo Nation","http://www.navajocourts.org/",None]
keychain["us;federal;courts.martial"] = ["us;federal;courts.martial","United States Courts Martial","http://en.wikipedia.org/wiki/Courts-martial_in_the_United_States",None]
keychain["us;federal;high.court.american.samoa"] = ["us;federal;high.court.american.samoa","High Court of American Samoa","http://en.wikipedia.org/wiki/High_Court_of_American_Samoa",None]

def mkCourt(key):
    if remap.has_key(key):
        key = remap[key]
    if keychain.has_key(key):
        return keychain[key]
    else:
        print "OUCH: " + key
        sys.exit()

for key in data:
    rptr = data[key]
    for obj in rptr:
        for jdct in obj["mlz_jurisdiction"]:
            
            # Convert jdct as soon as possible. Canonical forms only in code.
            jdct = mkCourt(jdct)[0]

            if not jurisdictions.has_key(jdct):
                jurisdictions[jdct] = {}
                jurisdictions[jdct]["name"] = mkCourt(jdct)[1]
                jurisdictions[jdct]["reporters"] = []
            variations = {}
            for variation in obj["variations"].keys():
                variation_target = obj["variations"][variation]
                if not variations.has_key(variation_target):
                    variations[variation_target] = []
                variations[variation_target].append(variation)
            for ekey in obj["editions"]:
                edition_orig = obj["editions"][ekey]
                edition = {}
                edition["title"] = ekey
                if edition_orig[0]["year"] == False:
                    edition["start"] = "present"
                else:
                    edition["start"] = "%d/%d/%d" % (edition_orig[0]["year"],edition_orig[0]["month"]+1,edition_orig[0]["day"])
                if edition_orig[1]["year"] == False:
                    edition["end"] = "present"
                else:
                    edition["end"] = "%d/%d/%d" % (edition_orig[1]["year"],edition_orig[1]["month"]+1,edition_orig[1]["day"])
                edition["name"] = obj["name"]
                edition["edition-abbreviation"] = ekey
                if obj["cite_type"] == "neutral":
                    edition["neutral"] = True
                else:
                    edition["neutral"] = False
                edition["flp-series-cite-type"] = obj["cite_type"]
                if variations.has_key(ekey):
                    edition["variations"] = variations[ekey]
                else:
                    edition["variations"] = []

                edition["common-key"] = key

                jurisdictions[jdct]["reporters"].append(edition)
    
def sortcourts (a,b):
    fedA = False
    fedB = False
    a = re.sub(";ca([0-9])$",";ca0\\1",a)
    b = re.sub(";ca([0-9])$",";ca0\\1",b)
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

def getPathFromCourtId(toppath,key=None):
    pth = ["data",toppath]
    if key:
        stub = key.split(";")
        pth.extend(stub)
    return os.path.sep.join(pth)

def writeToHierarchy(toppath,jkey,content):
    # Oh. It's not using jkey for shit.
    if toppath == "courts":
        jkey = mkCourt(jkey)[0]
    pth = getPathFromCourtId(toppath,key=jkey)
    try:
        os.makedirs(pth)
    except:
        pass
    open(os.path.join(pth,"index.txt"),"w+").write(content)
    

jkeys = []
for jkey in jurisdictions:
    jkeys.append(jkey)

def findCommonValue(jurisdictions):
    commonvalue = 0
    for i in range(0,minval,1):
        for j in range(0,len(jurisdictions)-1,1):
            if jurisdictions[j][i] != jurisdictions[j+1][i]:
                return commonvalue
        commonvalue += 1
    return commonvalue

jkeys.sort(sortcourts)
names = {}
for jkey in jkeys:
    jurisdiction = jurisdictions[jkey]
    reporters = []
    for reporter in jurisdiction["reporters"]:
        reporters.append(reporter)
    reporters.sort(sortreporters)

    abbrevs = [];
    for reporter in reporters:
        abbrevs.append(reporter["edition-abbreviation"])
        if reporter["neutral"]:
            neutral = "   :neutral:\n"
        else:
            neutral = ""
        
        str = '.. reporter:: %s\n   :flp-series-cite-type: %s\n   :flp-common-abbreviation: %s\n   :edition-abbreviation: %s\n   :dates: %s-%s\n%s' % (reporter["name"],reporter["flp-series-cite-type"],reporter["common-key"],reporter["edition-abbreviation"],reporter["start"],reporter["end"],neutral)
        sys.stdout.write(".")

        for variation in reporter["variations"]:
            str += "\n   .. variation:: %s\n" % variation

        rkey = "%s::%s" % (reporter["name"],reporter["edition-abbreviation"])
        reporter_key = reporter["name"] + "::" + reporter["edition-abbreviation"]
        if not names.has_key(reporter_key):
            names[reporter_key] = {"content":str,"jurisdictions":[],"abbrev":reporter["edition-abbreviation"]}
        jurisdiction = mkCourt(jkey)[0].split(";")
        names[reporter_key]["jurisdictions"].append(jurisdiction)

    # Write the court into the courts hierarchy here
    abbrevs.sort()
    if len(abbrevs):
        abbrevs = '\n   .. reporter-key:: ' + '\n\n   .. reporter-key:: '.join(abbrevs) + '\n'
    
    courtkey,name,url,flp_key = mkCourt(jkey)

    if flp_key:
        flp_key = '   :flp-key: ' + flp_key + '\n'

    str = '\n.. court:: %s\n   :court-id: %s\n   :url: %s\n%s%s' % (name,courtkey,url,flp_key,abbrevs)
    sys.stdout.write("+")
    writeToHierarchy("courts",courtkey,str)

# Fill out with courts that have not yet got any reporter keys

for key in keychain:
    # Get path from [0], get full name from [1]
    pth = getPathFromCourtId("courts",key=keychain[key][0])
    if not os.path.exists(os.path.join(pth,"index.txt")):
        # Create the file - with the court URL?
        #print "Create: " + pth + "/index.txt"

        if keychain[key][2]:
            url = '   :url: ' + keychain[key][2] + "\n"
        if keychain[key][3]:
            flp_key = '   :flp-key: ' + keychain[key][3] + '\n'

        content = "\n.. court:: %s\n   :court-id: %s\n%s" % (keychain[key][1],keychain[key][0],url,flp_key)
        writeToHierarchy("courts",keychain[key][0],content)

# Normalize each reporter to a single jurisdiction level
for key in names:
    # print key
    name = names[key]

    minval = None

    for i in range(0,len(name["jurisdictions"]),1):
        if minval == None or minval > len(name["jurisdictions"][i]):
            minval = len(name["jurisdictions"][i])
    for i in range(0,len(name["jurisdictions"]),1):
        name["jurisdictions"][i] = name["jurisdictions"][i][0:minval]
    # Find the maximum shared length of jurisdiction lists
    commonval = findCommonValue(name["jurisdictions"])
    name["jurisdictions"] = [name["jurisdictions"][0][0:commonval]]

# Write the reporters into the reporters hierarchy here.
for key in names:
    name = names[key]
    newkey = "%s;%s" % (";".join(name["jurisdictions"][0]),name["abbrev"])
    writeToHierarchy("reporters",newkey,name["content"])

print ""

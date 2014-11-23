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
        "us;federal;supreme.court": ["us;federal;supreme.court", "United States Supreme Court"],
        "us;federal;1-cir": ["us;federal;ca1", tmpl % ords[0]],
        "us;federal;2-cir": ["us;federal;ca2", tmpl % ords[1]],
        "us;federal;3-cir": ["us;federal;ca3", tmpl % ords[2]],
        "us;federal;4-cir": ["us;federal;ca4", tmpl % ords[3]],
        "us;federal;5-cir": ["us;federal;ca5", tmpl % ords[4]],
        "us;federal;6-cir": ["us;federal;ca6", tmpl % ords[5]],
        "us;federal;7-cir": ["us;federal;ca7", tmpl % ords[6]],
        "us;federal;8-cir": ["us;federal;ca8", tmpl % ords[7]],
        "us;federal;9-cir": ["us;federal;ca9", tmpl % ords[8]],
        "us;federal;10-cir": ["us;federal;ca10", tmpl % ords[9]],
        "us;federal;11-cir": ["us;federal;ca11", tmpl % ords[10]],
        "us;ak": ["us;ak;supreme.court", "Supreme Court of Alaska"], 
        "us;al": ["us;al;supreme.court", "Supreme Court of Alabama"], 
        "us;ar": ["us;ar;supreme.court", "Supreme Court of Arkansas"], 
        "us;az": ["us;az;supreme.court", "Supreme Court of Arizona"], 
        "us;ca": ["us;ca;supreme.court", "Supreme Court of California"], 
        "us;co": ["us;co;supreme.court", "Supreme Court of Colorado"], 
        "us;ct": ["us;ct;supreme.court", "Supreme Court of Connecticut"], 
        "us;dc": ["us;dc;court.of.appeals", "District of Columbia Court of Appeals"], 
        "us;de": ["us;de;supreme.court", "Supreme Court of Delaware"], 
        "us;fl": ["us;fl;supreme.court", "Supreme Court of Florida"], 
        "us;ga": ["us;ga;supreme.court", "Supreme Court of Georgia"], 
        "us;hi": ["us;hi;supreme.court", "Supreme Court of Hawaii"], 
        "us;ia": ["us;ia;supreme.court", "Supreme Court of Iowa"], 
        "us;id": ["us;id;supreme.court", "Supreme Court of Idaho"], 
        "us;il": ["us;il;supreme.court", "Supreme Court of Illinois"], 
        "us;in": ["us;in;supreme.court", "Supreme Court of Indiana"], 
        "us;ks": ["us;ks;supreme.court", "Supreme Court of Kansas"], 
        "us;ky": ["us;ky;supreme.court", "Supreme Court of Kentucky"], 
        "us;la": ["us;la;supreme.court", "Supreme Court of Louisiana"], 
        "us;ma": ["us;ma;supreme.court", "Supreme Court of Massachusetts"], 
        "us;md": ["us;md;supreme.court", "Supreme Court of Maryland"], 
        "us;me": ["us;me;supreme.court", "Supreme Court of Maine"], 
        "us;mi": ["us;mi;supreme.court", "Supreme Court of Michigan"], 
        "us;mn": ["us;mn;supreme.court", "Supreme Court of Minnisota"], 
        "us;mo": ["us;mo;supreme.court", "Supreme Court of Missouri"], 
        "us;ms": ["us;ms;supreme.court", "Supreme Court of Mississippi"], 
        "us;mt": ["us;mt;supreme.court", "Supreme Court of Montana"], 
        "us;nc": ["us;nc;supreme.court", "Supreme Court of North Carolina"], 
        "us;nd": ["us;nd;supreme.court", "Supreme Court of North Dakota"], 
        "us;ne": ["us;ne;supreme.court", "Supreme Court of Nebraska"], 
        "us;nh": ["us;nh;supreme.court", "Supreme Court of New Hampshire"], 
        "us;nj": ["us;nj;supreme.court", "Supreme Court of New Jersey"], 
        "us;nm": ["us;nm;supreme.court", "Supreme Court of New Mexico"], 
        "us;nv": ["us;nv;supreme.court", "Supreme Court of Nevada"], 
        "us;ny": ["us;ny;court.of.appeals", "New York Court of Appeals"], 
        "us;oh": ["us;oh;supreme.court", "Supreme Court of Ohio"], 
        "us;ok": ["us;ok;supreme.court", "Supreme Court of Oklahoma"], 
        "us;or": ["us;or;supreme.court", "Supreme Court of Oregon"], 
        "us;pa": ["us;pa;supreme.court", "Supreme Court of Pennsylvania"], 
        "us;pr": ["us;pr;supreme.court", "Supreme Court of Puerto Rico"], 
        "us;ri": ["us;ri;supreme.court", "Supreme Court of Rhode Island"], 
        "us;sc": ["us;sc;supreme.court", "Supreme Court of South Carolina"], 
        "us;sd": ["us;sd;supreme.court", "Supreme Court of South Dakota"], 
        "us;tn": ["us;tn;supreme.court", "Supreme Court of Tennessee"], 
        "us;tx": ["us;tx;supreme.court", "Supreme Court of Texas"], 
        "us;ut": ["us;ut;supreme.court", "Supreme Court of Utah"], 
        "us;va": ["us;va;supreme.court", "Supreme Court of Virginia"], 
        "us;vt": ["us;vt;supreme.court", "Supreme Court of Vermont"], 
        "us;wa": ["us;wa;supreme.court", "Supreme Court of Washington"], 
        "us;wi": ["us;wi;supreme.court", "Supreme Court of Wisconsin"], 
        "us;wv": ["us;wv;supreme.court", "Supreme Court of West Virginia"], 
        "us;wy": ["us;wy;supreme.court", "Supreme Court of Wyoming"]
        }
    if keychain.has_key(key):
        return keychain[key]
    else:
        return [key,key]

for key in data:
    rptr = data[key]
    for obj in rptr:
        for jdct in obj["mlz_jurisdiction"]:
            if not jurisdictions.has_key(jdct):
                jurisdictions[jdct] = {}
                jurisdictions[jdct]["name"] = mkCourt(jdct)[1]
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

def writeToHierarchy(toppath,jkey,content):
    jkey = mkCourt(jkey)[0]
    pth = ["data",toppath]
    jpth = jkey.split(";")
    pth.extend(jpth)
    pth = os.path.sep.join(pth)
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
        #reporter = jurisdiction["reporters"][rkey]
        abbrevs.append(reporter["series-abbreviation"])
        if reporter["neutral"]:
            neutral = "   :neutral:\n"
        else:
            neutral = ""
        
        str = '.. reporter:: %s\n   :series-abbreviation: %s\n   :dates: %s-%s\n%s\n' % (reporter["name"],reporter["series-abbreviation"],reporter["start"],reporter["end"],neutral)
        sys.stdout.write(".")

        rkey = "%s::%s" % (reporter["name"],reporter["series-abbreviation"])
        reporter_key = reporter["name"] + "::" + reporter["series-abbreviation"]
        if not names.has_key(reporter_key):
            names[reporter_key] = {"content":str,"jurisdictions":[],"abbrev":reporter["series-abbreviation"]}
        jurisdiction = mkCourt(jkey)[0].split(";")
        names[reporter_key]["jurisdictions"].append(jurisdiction)

    # Write the court into the courts hierarchy here
    abbrevs.sort()
    abbrevs = '\n\n   .. reporter-key:: '.join(abbrevs)

    courtkey = mkCourt(jkey)[0]
    
    str = '\n.. court:: %s\n   :court-id: %s\n\n   .. reporter-key:: %s\n' % (jurisdictions[jkey]["name"],courtkey,abbrevs)
    sys.stdout.write("+")
    writeToHierarchy("courts",jkey,str)

# Normalize each reporter to a single jurisdiction level
for key in names:
    print key
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

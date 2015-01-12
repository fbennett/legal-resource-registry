#!/usr/bin/python

import sys,os,json,re

pth = os.path.split(sys.argv[0])[0]
pth = os.path.join(pth,"..")
pth = os.path.abspath(pth)

modpath = os.path.join(pth,"lib")
sys.path.extend([modpath])

import readchar

ifh = open("courts.json")
ifh.seek(0)
obj = json.loads(ifh.read())
ifh.close()

jurisdiction_map = {
    "u": "us;"
}

#    "Puerto Rico": "pr", 


states_map = {
    "Alaska": "ak",  
    "Alabama": "al", 
    "Arkansas": "ar", 
    "Arizona": "az", 
    "California": "ca", 
    "Colorado": "co", 
    "Connecticut": "ct", 
    "Delaware": "de", 
    "Florida": "fl", 
    "Georgia": "ga", 
    "Hawaii": "hi", 
    "Iowa": "ia", 
    "Idaho": "id", 
    "Illinois": "il", 
    "Indiana": "in", 
    "Kansas": "ks", 
    "Kentucky": "ky", 
    "Louisiana": "la", 
    "Massachusetts": "ma", 
    "Maryland": "md", 
    "Maine": "me", 
    "Michigan": "mi", 
    "Minnesota": "mn", 
    "Missouri": "mo", 
    "Mississippi": "ms", 
    "Montana": "mt", 
    "North Carolina": "nc", 
    "North Dakota": "nd", 
    "Nebraska": "ne", 
    "New Hampshire": "nh", 
    "New Jersey": "nj", 
    "New Mexico": "nm", 
    "Nevada": "nv", 
    "New York": "ny", 
    "Ohio": "oh", 
    "Oklahoma": "ok", 
    "Oregon": "or", 
    "Pennsylvania": "pa", 
    "Rhode Island": "ri", 
    "South Carolina": "sc", 
    "South Dakota": "sd", 
    "Tennessee": "tn", 
    "Texas": "tx", 
    "Utah": "ut", 
    "Virginia": "va", 
    "Vermont": "vt", 
    "Washington": "wa", 
    "Wisconsin": "wi", 
    "West Virginia": "wv", 
    "Wyoming": "wy"
    }

nums = {
    "first": "1",
    "second": "2",
    "third": "3",
    "fourth": "4",
    "fifth": "5",
    "sixth": "6",
    "seventh": "7",
    "eighth": "8",
    "ninth": "9",
    "tenth": "10",
    "eleventh": "11"
    }

numrex = "(" + "|".join(nums.keys()) + ")"

def numsubber (m):
    return nums[m.group(1)]

rex = []
for key in states_map.keys() + ["United States","U\.S\."]:
    rex.append(key)
rex.sort()
#rex = "(.*?)(?<!D. )(?:" + "|".join(rex) + ")(.*)"
rex = "(" + "|".join(rex) + ")"

errata = open("ERRATA.txt","w+")

federalRex = ".*(U\.S\.|United States|D\.).*"

def sortByLength(a,b):
    if len(a) > len(b):
        return -1
    elif len(a) < len(b):
        return 1
    else:
        return 0
state_keys = states_map.keys()
state_keys.sort(sortByLength)

stateRex = ".*?(" + "|".join(state_keys) + ").*"

count = 0
for i in range(0,len(obj),1):
    name = obj[i]["fields"]["full_name"]
    print "(" + name + ")"
    count += 1
    while 1:
        prefix = ""
        jurisdiction = readchar.readchar()
        if jurisdiction == "\x03": sys.exit()
        if jurisdiction_map.has_key(jurisdiction):
            mFed = re.match(federalRex, name)
            mState = re.match(stateRex,name)
            if mFed:
                prefix = "us;federal;"
            if mState and not mFed:
                prefix = "us;" + states_map[mState.group(1)] + ";"
            if mState and mFed:
                prefix = "us;federal;" + states_map[mState.group(1)] + ";"
            if not mFed and not mState:
                prefix = "us;federal;"
            if name.find("West Virginia") > -1:
                print "GOTCHA *************************************************************************"
            #print jurisdiction_map[jurisdiction]
            if (re.match("^\s+.*",name)):
                errata.write(name.strip() + "\n   (leading spaces on name)\n\n")
            if (re.match(".*U\.S\..*",name)):
                errata.write(name.strip() + "\n   (U.S. instead of United States)\n\n")
            name = name.strip()
            m = re.match(".*?" + rex + ".*",name)
            if m:
                name = re.sub(rex,"",name)
            name = re.sub(" [a-z]+(?= )"," ",name)
            name = re.sub("\s+"," ",name)
            name = re.sub("[',.]","",name)
            name = name.lower().strip()
            name = re.sub(numrex,numsubber,name)
            name = re.sub("\.","",name)
            name = re.sub(" ",".",name)
            name = re.sub("(.*)\.([a-z]{0,1}d)$", "\\2.\\1", name)
            name = re.sub("^([a-z]{0,1}d)\.(.*)", "\\1;\\2", name)
            mlz_jurisdiction = "%s%s" % (prefix,name)
            print "  %d: %s" % (count,mlz_jurisdiction)
            obj[i]["fields"]["mlz_jurisdiction"] = mlz_jurisdiction
            break
        else:
            continue

ofh = open("courts-new.json","w+")

ofh.write(json.dumps(obj,indent=2))
ofh.close()

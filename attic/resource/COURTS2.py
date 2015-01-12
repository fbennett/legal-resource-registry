#!/usr/bin/python

#!/usr/bin/python

import sys,os,json,re

pth = os.path.split(sys.argv[0])[0]
pth = os.path.join(pth,"..")
pth = os.path.abspath(pth)

modpath = os.path.join(pth,"lib")
sys.path.extend([modpath])

import readchar

ifh = open("courts-new.json")
ifh.seek(0)
obj = json.loads(ifh.read())
ifh.close()

def sortme(a,b):
    a = a["fields"]["mlz_jurisdiction"]
    b = b["fields"]["mlz_jurisdiction"]
    aJur = re.sub("^(.*);.*","\\1",a)
    bJur = re.sub("^(.*);.*","\\1",b)
    aSupreme = (a.find(";supreme.court") > -1 or a.find("ny;court.appeals") > -1)
    bSupreme = (b.find(";supreme.court") > -1 or b.find("ny;court.appeals") > -1)
    if aJur == bJur and (aSupreme or bSupreme):
        if aSupreme:
            return -1
        else:
            return 1
    if a > b:
        return 1
    elif a < b:
        return -1
    else:
        return 0

obj.sort(sortme)

state_jur_map = {}

last_jurisdiction = None
for i in range(0,len(obj),1):
    jurisdiction = obj[i]["fields"]["mlz_jurisdiction"]
    fields = obj[i]["fields"]
    state_jur_map[jurisdiction] = [fields["mlz_jurisdiction"],fields["full_name"],fields["url"],obj[i]["pk"]]
    if jurisdiction.startswith("us;federal;"):
        continue
    m = re.match("^(us;[a-z]{2}(?=;)).*",jurisdiction)
    if m:
        this_jurisdiction = m.group(1)
    if this_jurisdiction != last_jurisdiction:
        # print fields["mlz_jurisdiction"].upper()
        state_jur_map[this_jurisdiction] = [fields["mlz_jurisdiction"],fields["full_name"],fields["url"],obj[i]["pk"]]
    else:
        #print "  " + fields["mlz_jurisdiction"]
        pass
    last_jurisdiction = this_jurisdiction

open("state_jur_map.json","w+").write(json.dumps(state_jur_map,indent=2))

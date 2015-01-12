#!/usr/bin/python
#-*- encoding: utf-8 -*-

import sys,os,re,json

NAMES = json.loads(open("NAMES.json").read())

COURT_TYPES = {
    "家庭": "Family",
    "地方": "District"
}

for d in os.listdir("."):
    if not os.path.isdir(d): continue
    for f in os.listdir(d):
        ifh = open(os.path.join(d,f))
        txt = ""
        name = None
        court_type = None
        court = None
        while True:
           line = ifh.readline()
           if not line: break
           if line.startswith(".. court::"):
               data = line[10:].strip()
               m = re.match("(.*)(家庭|地方)(裁判所)",data)
               if m:
                   name = m.group(1).decode("utf-8")
                   court_type = m.group(2)
                   court = m.group(3)
               line = line + "   :en: " + NAMES[name] + " " + COURT_TYPES[court_type] + " Court\n"
           txt += line
        ifh.close()
        txt = txt.strip()
        ofh = open(os.path.join(d,f), "w+")
        ofh.write(txt + "\n")

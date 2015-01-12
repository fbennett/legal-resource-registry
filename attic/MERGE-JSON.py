#!/usr/bin/python

import sys,os,re,json

obj = json.loads(open("ALL-COURTS.json").read())

country_template = '''
.. country:: %s
'''

court_template = '''
.. court:: %s
   :court-id: %s
   :url: %s%s
'''

for key in obj.keys():
    keylst = key.lower().split("-")
    if keylst[0] == "us" or keylst[0] == "jp": continue

    keypth = "/".join(keylst)
    ctypth = os.path.join("data", "courts", keypth)

    try:
        os.makedirs(ctypth)
    except:
        pass
    country_name = obj[key]["country-name"]
    open(os.path.join(ctypth, "index.txt"), "w+").write(country_template % country_name)
    #print country_name

    for ctkey in obj[key]["courts"]:
        ctpth = os.path.join(keypth, ctkey, "index.txt")

        #print "  " + ctpth

        ctobj = obj[key]["courts"][ctkey]
        if not ctobj.has_key("local"):
            court_name = ctobj["en"]
            court_name_en = ""
        else:
            court_name = ctobj["local"]
            court_name_en = "\n   :en: %s" % ctobj["en"]
        if not ctobj.has_key("url"):
            print "%s has no URL" % country_name
            continue
        court_url = ctobj["url"]
        court_id = ";".join(keylst + [ctkey])
        
        #print court_template % (court_name, court_id, court_url, court_name_en)

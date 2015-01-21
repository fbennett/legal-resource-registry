'''
   Legal Resource Registry export config module for Free Law Project
'''

import json
from LRR.traveler import Opt
from LRR.utils import Utils

class Data:
    def __init__(self):
        self.categories = {}

class Hook(Utils):
    
    def __init__(self):
        self.data = Data()
        self.opt = Opt()
        self.opt.jurisdiction = "jp"

    def variation(self, arg):
        pass

    def court(self, options, arg):
        courtID = options["court-id"]
        courtLst = self.splitUrn(courtID)
        courtKey = courtLst.pop()
        categoryID = self.joinUrn(courtLst)
        if not self.data.categories.has_key(categoryID):
            self.data.categories[categoryID] = {}
        self.data.categories[categoryID][courtID] = {}
        self.data.categories[categoryID][courtID]["local"] = arg
        self.data.categories[categoryID][courtID]["url"] = options["url"]
        self.data.categories[categoryID][courtID]["en"] = options["en"]
        courtKey = courtKey.split(".")
        for i in range(0,len(courtKey),1):
            courtKey[i] = courtKey[i][0].upper() + courtKey[i][1:]
        courtKey = " ".join(courtKey)
        self.data.categories[categoryID][courtID]["roman"] = courtKey


    def reporter_start(self, options, dates, arg):
        pass

    def reporter_end(self, options, arg):
        pass

    def export(self):
        obj = {
            "JP":{
                "country-name": "Japan",
                "courts": self.data.categories
                }
            }

        open("jp_courts.json","w+").write(json.dumps(obj,indent=2,sort_keys=True))

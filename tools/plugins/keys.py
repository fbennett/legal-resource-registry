from LRR import Hook as HookBase
import json, os, re

class MyAmazingDataClass:
    def __init__(self):
        self.place_keys = {}
        self.court_keys = {}

class Hook(HookBase):
    def __init__(self):
        HookBase.__init__(self, Data=MyAmazingDataClass)
        #self.opt.jurisdiction = "gb" 

    def category(self, options, arg):
        ''' Note: There is no category directive in the rST.
        This is run by pages.py during the primitive parse there.
        '''
        categoryID = options["category-id"]
        categoryPath = categoryID.replace(";", "/")
        dirPath = os.path.join("data/courts", categoryPath)
        count = 0
        for fileName in os.listdir(dirPath):
            if not os.path.isdir(os.path.join(dirPath, fileName)): continue
            count += 1
        if count == 0 or categoryPath.find("/") == -1:
            self.data.place_keys[categoryID] = arg

    def court(self, options, arg):
        courtID = options["court-id"]
        self.data.court_keys[courtID] = arg
        placeID = ";".join(courtID.split(";")[0:-1])
        #if placeID == "us;federal": return
        countryID = courtID.split(";")[0]
        if not self.data.place_keys.has_key(countryID):
            txt = open(os.path.join("data/courts", countryID, "index.txt")).read().strip()
            m = re.match("(?m)^\.\. category::\s*(.*)$", txt)
            countryName = m.group(1)
            self.data.place_keys[countryID] = countryName
        if not self.data.place_keys.has_key(placeID):
            txt = open(os.path.join("data/courts", "/".join(placeID.split(";")), "index.txt")).read().strip()
            m = re.match("(?m)^\.\. category::\s*(.*)$", txt)
            placeName = m.group(1)
            self.data.place_keys[placeID] = placeName

    def reporter_start(self, options, dates, arg):
        pass

    def reporter_end(self, options, arg):
        pass

    def variation(self, arg):
        pass

    def export(self):
        open("rebuild-ids/key-courts.json", "w+").write(json.dumps(self.data.court_keys, sort_keys=True, indent=2, ensure_ascii=False))
        countries = json.loads(open("tools/country-names.json").read())
        for key in countries.keys():
            lowKey = key.lower()
            if not self.data.place_keys.has_key(lowKey):
                self.data.place_keys[lowKey] = countries[key]
        open("rebuild-ids/key-places.json", "w+").write(json.dumps(self.data.place_keys, sort_keys=True, indent=2, ensure_ascii=False))


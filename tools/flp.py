'''
   Legal Resource Registry export config module for Free Law Project
'''

import json

class Data:
    def __init__(self):
        self.variations = {}
        self.jurisdiction = None
        self.courts_map = {}
        self.reporters_json = {}
        self.series = None
        self.edition_key = None

class Hook:
    
    def __init__(self):
        self.data = Data()

    def variation(self, arg):
        self.data.variations[arg] = True
        pass

    def court(self, options):
        self.data.jurisdiction = options["court-id"]
        if options.has_key("flp-key"):
            self.data.courts_map[options["flp-key"]] = options["court-id"]

    def reporter_start(self, dates, arg, options):
        if options.has_key("flp-common-abbreviation"):
            bundle_key = options["flp-common-abbreviation"]
            if not self.data.reporters_json.has_key(bundle_key):
                bundle = []
                self.data.reporters_json[options["flp-common-abbreviation"]] = bundle
            else:
                bundle = self.data.reporters_json[bundle_key]
            series_name = arg
            edition_key = options["edition-abbreviation"]
                
            series = self.findReporterSeries(bundle,series_name)
            if not series:
                series = {}
                series["cite_type"] = options["flp-series-cite-type"]
                series["editions"] = {}
                series["mlz_jurisdiction"] = []
                series["name"] = series_name
                series["variations"] = {}
                bundle.append(series)
            if not series["mlz_jurisdiction"].count(self.data.jurisdiction):
                series["mlz_jurisdiction"].append(self.data.jurisdiction)
                series["mlz_jurisdiction"].sort()
            if dates.endYear:
                end = "%02d-%02d-%02dT00:00:00" % (int(dates.endYear),int(dates.endMonth),int(dates.endDay))
            else:
                end = None
            series["editions"][edition_key] = {
                "end": end,
                "start": "%02d-%02d-%02dT00:00:00" % (int(dates.startYear),int(dates.startMonth),int(dates.startDay))
                }
            self.data.series = series
            self.data.edition_key = edition_key

    def reporter_end(self, arg, options):
        if options.has_key("flp-common-abbreviation"):
            for key in self.data.variations.keys():
                self.data.variations[key] = self.data.edition_key
            self.data.series["variations"].update(self.data.variations)
            self.data.variations = {}
            self.data.series = None
            self.data.edition_key = None

    def findReporterSeries(self,bundle,name):
        for series in bundle:
            if series["name"] == name:
                return series
        return False

    def export(self):
        def sortrep(a,b):
            if a["name"] > b["name"]:
                return 1
            elif a["name"] < b["name"]:
                return -1
            else:
                return 0

        for key in self.data.reporters_json.keys():
            bundle = self.data.reporters_json[key]
            bundle.sort(sortrep)
            for series in bundle:
                series["mlz_jurisdiction"].sort()

        open("reporters-db.json","w+").write(json.dumps(self.data.reporters_json,indent=2,sort_keys=True))
        open("courts-map-flp.json","w+").write(json.dumps(self.data.courts_map,indent=2,sort_keys=True))

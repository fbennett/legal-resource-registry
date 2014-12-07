'''
   Legal Resource Registry export config module for Free Law Project
'''

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

    def reporter_start(self, arg, options):
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
            if endyear:
                end = "%02d-%02d-%02dT00:00:00" % (int(endyear),int(endmonth),int(endday))
            else:
                end = None
            series["editions"][edition_key] = {
                "end": end,
                "start": "%02d-%02d-%02dT00:00:00" % (int(startyear),int(startmonth),int(startday))
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


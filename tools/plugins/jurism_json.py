from LRR import Hook as HookBase
from LRR.utils import Utils
import json

## Builds jurisdictions.json for jurism/resources/schema/jurisdictions.json

countries = json.loads(open("tools/country-names.json").read())

class Data:
    def __init__(self):
        self.jurisdictions = {}
        self.courts = {}

def sortTheList(a, b):
    if a[0] > b[0]:
        return 1
    elif a[0] < b[0]:
        return -1
    else:
        return 0

class Hook(HookBase, Utils):
    def __init__(self):
        HookBase.__init__(self, Data=Data)
        #self.opt.jurisdiction = "jp"
        pass

    def category(self, options, arg):
        ''' Note: There is no category directive in the rST.
        This is run by pages.py during the primitive parse there.
        '''
        jurisdictionID = options["category-id"]
        # We'll cumulate these, joining with pipes 
        self.data.jurisdictions[jurisdictionID] = arg

    # OK
    # courts
    # jurisdictions
    # courtNames
    # courtCountryLinks
    # courtJurisdictionLinks

    def court(self, options, arg):
        courtID = options['court-id']
        self.data.courts[courtID] = arg;

    def reporter_start(self, options, dates, arg):
        pass

    def reporter_end(self, options, arg):
        pass

    def variation(self, arg):
        pass

    def export(self):

        # XXX Export a compact JSON representation of the data
        # XXX that can be processed into jurisdiction and court
        # XXX lists in the MLZ client.

        srcList = []
        for countryKey in countries.keys():
            if not self.data.jurisdictions.has_key(countryKey.lower()):
                self.data.jurisdictions[countryKey.lower()] = countries[countryKey]
        for key in self.data.jurisdictions.keys():
            # If a country, set as "Japan|JP"
            # Otherwise, leave name untouched
            if key.find(":") == -1 and key.find(";") == -1:
                self.data.jurisdictions[key] = "%s|%s" % (self.data.jurisdictions[key],key.upper())
            name = self.data.jurisdictions[key]
            srcList.append([key, name])
        for key in self.data.courts.keys():
            name = self.data.courts[key]
            srcList.append([key, name])
        srcList.sort(sortTheList)
        fh = open("rebuild-ids/jurisdictions.json", "w+")
        output = {
            "jurisdictions":[],
            "courtNames": [],
            "countryCourtLinks": [],
            "courts": [],
            "courtJurisdictionLinks": []
        }
        jurisdictions_nummap = {}
        courtNames_nummap = {}
        countryCourtLinks_nummap = {}
        courts_nummap = {}
        for item in srcList:
            title = item[1]
            # Split into jurisdiction elements and courtID
            keyLst = item[0].split(";");

            jurisdiction = keyLst[0]
            jurisdictionLst = jurisdiction.split(":")
            if len(jurisdictionLst) == 1:
                jurisdictionParent = False
            else:
                jurisdictionParent = ":".join(jurisdictionLst[0:-1])
            jurisdictionStub = jurisdictionLst[-1]

            if len(keyLst) > 1:
                court = keyLst[1]
            else:
                court = False
            # Jurisdiction
            if not jurisdictions_nummap.has_key(jurisdiction):
                if jurisdictionParent:
                    jurisdictionParentIdx = jurisdictions_nummap[jurisdictionParent]
                    output["jurisdictions"].append([jurisdictionStub, title, jurisdictionParentIdx])
                else:
                    output["jurisdictions"].append([jurisdiction, title])
                jurisdictions_nummap[jurisdiction] = (len(output["jurisdictions"])-1)

            if court:
                # Court name
                if not courtNames_nummap.has_key(title):
                    output["courtNames"].append(title)
                    courtNames_nummap[title] = (len(output["courtNames"])-1)
                # index of court name and index of first jurisdiction element (country)
                courtNameIdx = courtNames_nummap[title]
                countryID = jurisdiction.split(":")[0]
                countryIdx = jurisdictions_nummap[countryID]
                mykey = "%d::%d" % (courtNameIdx,countryIdx)
                if not countryCourtLinks_nummap.has_key(mykey):
                    output["countryCourtLinks"].append([courtNameIdx, countryIdx])
                    countryCourtLinks_nummap[mykey] = (len(output["countryCourtLinks"])-1)
                # index of court name / country index. Very meta.
                countryCourtLinkIdx = countryCourtLinks_nummap[mykey]
                mykey2 = "%s::%d" % (court, countryCourtLinkIdx)
                if not courts_nummap.has_key(mykey2):
                    output["courts"].append([court, (len(output["countryCourtLinks"])-1)])
                    courts_nummap[mykey2] = (len(output["courts"])-1)
                # court jurisdiction links, which was what all of the above was aiming for
                jurisdictionIdx = jurisdictions_nummap[jurisdiction]
                courtIdx = courts_nummap[mykey2]
                output["courtJurisdictionLinks"].append([jurisdictionIdx, courtIdx])

        fh.write(json.dumps(output, ensure_ascii=False))
        #fh.write(json.dumps(output, sort_keys=True, indent=2, ensure_ascii=False))
        fh.close()

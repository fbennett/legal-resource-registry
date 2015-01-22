from LRR import Hook as HookBase
from LRR.utils import Utils
import json

countries = json.loads(open("tools/country-names.json").read())

class Data:
    def __init__(self):
        self.names = {}

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
        categoryID = options["category-id"]
        # We'll cumulate these, joining with pipes 
        self.data.names[categoryID] = arg

    def court(self, options, arg):
        pass

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

        theList = []
        for countryKey in countries.keys():
            if not self.data.names.has_key(countryKey.lower()):
                self.data.names[countryKey.lower()] = countries[countryKey]
        for key in self.data.names:
            # Split
            keyLst = self.splitUrn(key)
            nameLst = self.splitUrn(key)
            countryID = keyLst[0]
            # Iterate from start to end, making country ISO, others descrips
            for i in range(0, len(nameLst), 1):
                if i == 0:
                    nameLst[i] = nameLst[i].upper()
                else:
                    subkey = self.joinUrn(keyLst[0:i+1])
                    nameLst[i] = self.data.names[subkey]
            # Join with pipes
            nameLst = [self.data.names[countryID]] + nameLst
            name = '|'.join(nameLst)
            # Cast to template
            theList.append([key, name])
        theList.sort(sortTheList)
        fh = open("rebuild-ids/mlz-zls.sql", "w+")
        for item in theList:
            line = 'INSERT INTO jurisdictions VALUES("%s","%s");\n' % (item[0], item[1])
            fh.write(line)
        fh.close()

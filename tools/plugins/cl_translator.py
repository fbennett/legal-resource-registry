from LRR import Hook as HookBase
from LRR.utils import Utils
import json

class Data:
    def __init__(self):
        self.courts = {}
        self.missing = []

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
        self.opt.jurisdiction = "us"
        pass

    def court(self, options, arg):
        courtID = options['court-id']
        if not options.has_key("flp-key"):
            self.data.missing.append([courtID, arg])
        else:
            flpKey = options['flp-key']
            self.data.courts[flpKey] = [courtID, arg]

    def reporter_start(self, options, dates, arg):
        pass

    def reporter_end(self, options, arg):
        pass

    def variation(self, arg):
        pass

    def export(self):
        if len(self.data.missing):
            print "===================\nCourts without keys\n==================="
            for court in self.data.missing:
                print court[1]
                print "  " + court[0]
            print ""
        fh = open("for-court-listener-translator.js", "w+")
        fh.write("var court_ids = " + json.dumps(self.data.courts, sort_keys=True, ensure_ascii=False))
        #fh.write("var court_ids = " + json.dumps(self.data.courts, sort_keys=True, indent=2, ensure_ascii=False))
        fh.close()

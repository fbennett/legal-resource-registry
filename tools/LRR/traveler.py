'''
  Traveling object for Legal Resource Registry
'''

import imp,os,re
from utils import Utils

class Defaults:
    def __init__(self):
        self.required = {}
        self.optional = {}
        self.default = {}
        self.auxiliary = {}

    def __setitem__(self,seg,val):
        segment = getattr(self,seg)
        segment[val] = True

    def __getitem__(self,seg):
        return getattr(self,seg)

class Local:
    def __init__(self):
        self.required = {}
        self.optional = {}

    def __setitem__(self,seg,val):
        segment = getattr(self,seg)
        segment[val] = True

    def __getitem__(self,seg):
        return getattr(self,seg)

class Features:
    
    def __init__(self):
        self.defaults = Defaults()
        self.local = None

    def reset(self):
        self.local = None

    def set_base(self):
        self.local = Local()
        self.local.required = self.defaults.required.copy()
        self.local.optional = self.defaults.optional.copy()

    def set_defaults(self):
        self.local = Local()
        self.local.required = self.defaults.required.copy()
        self.local.required.update(self.defaults.default)
        self.local.optional = self.defaults.optional.copy()

class Data:
    def __init__(self):
        pass

class Opt:
    def __init__(self):
        self.jurisdiction = None

class Hook:
    def __init__(self):
        self.data = Data()
        self.opt = Opt()
        self.court = None
        self.reporter_start = None
        self.reporter_end = None
        self.variation = None
        self.export = None

class Traveler(Utils):
    def __init__(self):
        self.features = Features()
        self.gitHubStub = "https://github.com/fbennett/legal-resource-registry/tree/master/data"
        self.rootPath = self.getRootPath()
        self.hook = Hook()

    def setJurisdiction(self, jurisdiction):
        self.opt.jurisdiction = jurisdiction

    def setHook(self, plugin_name):

        class_inst = None
        expected_class = 'Hook'

        plugin_name = re.sub("\.(?:py|pyc)$", "", plugin_name)

        pathname = os.path.join(self.rootPath, "tools", "%s.py" % plugin_name)

        py_mod = imp.load_source(plugin_name, pathname)

        if hasattr(py_mod, expected_class):
            class_inst = getattr(py_mod, expected_class)()
            self.hook = class_inst
        else:
            print "Module %s not found." % expected_class

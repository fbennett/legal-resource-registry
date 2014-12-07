'''
  Traveling object for Legal Resource Registry
'''

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
        self.variations = {}
        self.jurisdiction = None
        self.courts_map = {}
        self.reporters_json = {}
        self.series = None
        self.edition_key = None

class Hook:
    def __init__(self):
        self.data = Data()
        self.court = None
        self.reporter_start = None
        self.reporter_end = None
        self.variation = None

class Traveler:
    def __init__(self):
        self.features = Features()
        self.reporters_json = {}
        self.courts_map = {}
        self.jurisdiction = []
        self.variations = {}
        self.gitHubStub = "https://github.com/fbennett/legal-resource-registry/tree/master/data"
        self.hook = Hook()



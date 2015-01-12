'''
   Legal Resource Registry export config module for page with U.S. neutral citation forms.
'''

import json
from LRR import Hook as HookBase

class Hook(HookBase):
    def __init__(self):
        HookBase.__init__(self)
        self.opt.jurisdiction = "us"
        self.opt.conditional = {
            "title": "U.S. Neutral Citations",
            "pageKey": "us-neutral.html",
            "condition": {
                "neutral": True
            }
        }

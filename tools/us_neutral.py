'''
   Legal Resource Registry export config module for Free Law Project
'''

import json
from LRR.traveler import Hook as DefaultHook

class Data:
    def __init__(self):
        self.variations = {}
        self.jurisdiction = None
        self.series = None
        self.edition_key = None
        self.single_page = '''
.. include:: /media/storage/src/legal-resource-registry/doc-src/fields.rst

.. include:: /media/storage/src/legal-resource-registry/doc-src/banner.rst

-----------------
Neutral Citations
-----------------

.. include:: /media/storage/src/legal-resource-registry/doc-src/draft-note.rst

.. include:: /media/storage/src/legal-resource-registry/doc-src/credits.rst

.. container:: back-button right

   .. image:: graphics/circle-arrow-down-white.png
      :target: index.html


.. container:: back-button left

   .. image:: graphics/circle-arrow-down-white.png
      :target: index.html



'''.lstrip()

class Hook(DefaultHook):
    
    def __init__(self):
        DefaultHook.__init__(self)
        self.opt.jurisdiction = "us"
        self.opt.condition = {
            "neutral": True
            }
        self.opt.pagename = "us-neutral.html"
        self.data = Data()

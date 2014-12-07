#!/usr/bin/python
#-*- encoding: utf-8 -*-
"""
A Docutils Publisher script for the Legal Resource Registry
"""

import re,os,os.path,sys

try:
    import locale
    locale.setlocale(locale.LC_ALL, '')
except:
    pass

pth = os.path.split(sys.argv[0])[0]
pth = os.path.join(pth,"..")
pth = os.path.abspath(pth)

from docutils.core import publish_cmdline, default_description
from docutils.parsers.rst import directives, roles, states
from docutils import nodes, statemachine
from docutils.writers.html4css1 import Writer
from LRR import *

directives.register_directive("bubble", BubbleDirective)
directives.register_directive("variation", VariationDirective)
directives.register_directive("reporter", ReporterDirective)
directives.register_directive("fields", FieldsDirective)
directives.register_directive("jurisdiction", JurisdictionDirective)
directives.register_directive("court", CourtDirective)
roles.register_local_role("trans", role_trans)

class reporterPathException(Exception):
    def __init__(self,jurisdiction,reporterKey):
        self.jurisdiction = jurisdiction
        self.reporterKey = reporterKey

class WriterForLegalCitem(Writer):
    def __init__(self):
        Writer.__init__(self)
        self.translator_class = HTMLTranslatorForLegalResourceRegistry

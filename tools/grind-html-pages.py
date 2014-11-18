#!/usr/bin/python

# $Id: rst2html.py 4564 2006-05-21 20:44:42Z wiemann $
# Author: David Goodger <goodger@python.org>
# Copyright: This module has been placed in the public domain.

"""
A minimal front end to the Docutils Publisher, producing HTML.
"""

import re,os,os.path,sys

try:
    import locale
    locale.setlocale(locale.LC_ALL, '')
except:
    pass

from docutils.core import publish_cmdline, default_description
from docutils.parsers.rst import directives, roles, states
from docutils import nodes
from docutils.writers.html4css1 import Writer, HTMLTranslator
from docutils.parsers.rst import Directive

class creditsbox (nodes.TextElement): pass
class citationgroup (nodes.TextElement): pass
class court (nodes.TextElement): pass
class notes (nodes.TextElement): pass
class courtid (nodes.TextElement): pass
class reporters (nodes.TextElement): pass
class reporterbox (nodes.TextElement): pass
class reporter (nodes.TextElement): pass
class reporterneutral (nodes.TextElement): pass
class reportername (nodes.TextElement): pass
class reporterdates (nodes.TextElement): pass
class descriptionbox (nodes.TextElement): pass
class featurebox (nodes.TextElement): pass
class bubble (nodes.Inline, nodes.TextElement): pass
class label (nodes.Inline, nodes.TextElement): pass
class value (nodes.Inline, nodes.TextElement): pass
class valueunconfirmed (nodes.Inline, nodes.TextElement): pass
class valueneutral (nodes.Inline, nodes.TextElement): pass
class featurename (nodes.Inline, nodes.TextElement): pass

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

    def set_base(self):
        self.local = Local()
        self.local.required = self.defaults.required.copy()
        self.local.optional = self.defaults.optional.copy()

    def set_defaults(self):
        self.local = Local()
        self.local.required = self.defaults.required.copy()
        self.local.required.update(self.defaults.default)
        self.local.optional = self.defaults.optional.copy()

FEATURES = Features()

class HTMLTranslatorForLegalCitem(HTMLTranslator):

    def __init__(self, document, **kwargs):
        HTMLTranslator.__init__(self, document, **kwargs)
        settings = self.settings
        #self.d_class = DocumentClass(settings.documentclass)

    def visit_creditsbox(self, node):
        self.body.append(self.starttag(node, 'div', CLASS="credits-box")+'<div>\n')

    def depart_creditsbox(self, node):
        self.body.append('</div>\n</div>\n')

    def visit_citationgroup(self, node):
        self.body.append(self.starttag(node, 'h2', CLASS="citation-group").strip())

    def depart_citationgroup(self, node):
        self.body.append('</h2>\n')

    def visit_court(self, node):
        self.body.append(self.starttag(node, 'h3', CLASS="court").strip())

    def depart_court(self, node): 
        self.body.append('</h3>\n')

    def visit_courtid(self, node):
        self.body.append(self.starttag(node, 'div', CLASS="court-id").strip())

    def depart_courtid(self, node): 
        self.body.append('</div>\n')

    def visit_reporters(self, node):
        self.body.append(self.starttag(node, 'div', CLASS="reporters"))

    def depart_reporters(self, node): 
        self.body.append('</div>\n')

    def visit_reporterbox(self, node):
        self.body.append(self.starttag(node, 'div', CLASS="reporter-box").strip())

    def depart_reporterbox(self, node): 
        self.body.append('</div>')

    def visit_reporter(self, node):
        self.body.append(self.starttag(node, 'div', CLASS="reporter"))

    def depart_reporter(self, node): 
        self.body.append('</div>\n')

    def visit_reporterneutral(self, node):
        self.body.append(self.starttag(node, 'div', CLASS="reporter neutral").strip())

    def depart_reporterneutral(self, node): 
        self.body.append('</div>')

    def visit_reportername(self, node):
        self.body.append(self.starttag(node, 'div', CLASS="reporter-name"))

    def depart_reportername(self, node): 
        self.body.append('</div>\n')

    def visit_reporterdates(self, node):
        self.body.append(self.starttag(node, 'div', CLASS="reporter-dates"))

    def depart_reporterdates(self, node): 
        self.body.append('</div>\n')

    def visit_notes(self, node):
        self.body.append(self.starttag(node, 'div', CLASS="notes"))

    def depart_notes(self, node): 
        self.body.append('</div>\n')

    def visit_seriesabbrev(self, node):
        self.body.append(self.starttag(node, 'div', CLASS="notes"))

    def depart_seriesabbrev(self, node): 
        self.body.append('</div>\n')

    def visit_dates(self, node):
        self.body.append(self.starttag(node, 'div', CLASS="notes"))

    def depart_dates(self, node): 
        self.body.append('</div>\n')

    def visit_bubble(self, node):
        self.body.append('<span class="bubble">')

    def depart_bubble(self, node): 
        self.body.append('</span>')

    def visit_descriptionbox(self, node):
        self.body.append(self.starttag(node, 'div', CLASS="description-box"))

    def depart_descriptionbox(self, node): 
        self.body.append('</div>')

    def visit_featurebox(self, node):
        self.body.append(self.starttag(node, 'div', CLASS="feature-box"))

    def depart_featurebox(self, node): 
        self.body.append('</div>')

    def visit_label(self, node):
        self.body.append('<span class="label">')

    def depart_label(self, node): 
        self.body.append('</span>')

    def visit_value(self, node):
        self.body.append('<span class="value">')

    def depart_value(self, node): 
        self.body.append('</span>')

    def visit_valueunconfirmed(self, node):
        self.body.append('<span class="value unconfirmed">')

    def depart_valueunconfirmed(self, node): 
        self.body.append('</span>')

    def visit_valueneutral(self, node):
        self.body.append('<span class="value neutral">')

    def depart_valueneutral(self, node): 
        self.body.append('</span>')

    def visit_featurename(self, node):
        self.body.append('<span class="feature-name">')

    def depart_featurename(self, node): 
        self.body.append('</span>')

class CreditsDirective(Directive):
    required_arguments = 0
    optional_arguments = 0
    has_content = True
    option_spec = {}

    def run (self):
        nodes = creditsbox()
        self.state.nested_parse(self.content, self.content_offset,
                                nodes)
        return [nodes]

class FieldsDirective(Directive):
    required_arguments = 0
    optional_arguments = 0
    has_content = True
    option_spec = {}

    def run (self):
        features = {}
        if not FEATURES.local:
            for line in self.content:
                m = re.match("^:([a-z][-a-z]+):\s+(default|auxiliary|required|optional)",line)
                if not m:
                    error = self.state_machine.reporter.error(
                        'Invalid context: syntax error in option to initial fields directive',
                        nodes.literal_block(self.block_text, self.block_text), line=self.lineno)
                    return [error]
                FEATURES.defaults[m.group(2)] = m.group(1)
                FEATURES.set_defaults()
        else:
            FEATURES.set_base()
            for line in self.content:
                m = re.match("^:([a-z][-a-z]+):\s+(required|optional)",line)
                if not m:
                    error = self.state_machine.reporter.error(
                        'Invalid context: syntax error in option to subsequent fields directive. Note that default and auxiliary cannot be used here.',
                        nodes.literal_block(self.block_text, self.block_text), line=self.lineno)
                    return [error]
                if not FEATURES.defaults.auxiliary.has_key(m.group(1)) and not FEATURES.defaults.optional.has_key(m.group(1))  and not FEATURES.defaults.default.has_key(m.group(1)):
                    error = self.state_machine.reporter.error(
                        'Invalid context: undefined field in subsequent fields directive. Only fields initially declared as default, optional or auxiliary may be declared. line=%s' % self.lineno,
                        nodes.literal_block(self.block_text, self.block_text), line=self.lineno)
                    return [error]
                FEATURES.local[m.group(2)] = m.group(1)
        return []

class CitationGroupDirective(Directive):
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    has_content = True
    option_spec = {}

    def run (self):
        newnode = citationgroup(rawsource=self.arguments[0],text=self.arguments[0])
        content = '\n'.join(self.content)
        newnodes = nodes.generated(rawsource=content)
        self.state.nested_parse(self.content, self.content_offset,
                                newnodes)
        return [newnode,newnodes]

class CourtDirective(Directive):
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    has_content = True
    option_spec = {
        'court-id': directives.unchanged
    }
    def run (self):
        if not self.options.has_key('court-id'):
            error = self.state_machine.reporter.error(
                'Invalid context: missing court-id option in court directive',
                nodes.literal_block(self.block_text, self.block_text), line=self.lineno)
            return [error]
        court_id_node = courtid()
        court_id_bubble = bubble(rawsource=self.options['court-id'],text=self.options['court-id'])
        court_id_node += court_id_bubble
        court_node = court(rawsource=self.arguments[0],text=self.arguments[0])

        # Split in two here, and validate.
        # notes:: is optional, must be the first element if present, and can occur only once. 
        # reporter:: is the only other permitted element.

        foundNotes = False
        foundReporter = False
        reporter_offset = 0
        for line in self.content:
            if line.startswith('.. reporter::'):
                foundReporter = True
            if line.startswith('.. notes::'):
                if foundReporter:
                    error = self.state_machine.reporter.error(
                        'Invalid structure: notes:: must come before any reporter:: in court directive',
                        nodes.literal_block(self.block_text, self.block_text), line=self.lineno)
                    return [error]
            if not foundReporter:
                reporter_offset += 1
        
        note_content = '\n'.join(self.content[0:reporter_offset])
        note_node = nodes.generated(rawsource=note_content)
        self.state.nested_parse(self.content[0:reporter_offset], self.content_offset,
                                note_node)

        reporter_content = '\n'.join(self.content[reporter_offset:])
        reporters_node = reporters()
        self.state.nested_parse(self.content[reporter_offset:], self.content_offset + reporter_offset,
                                reporters_node)

        return [court_node,court_id_node,note_node,reporters_node]

class ReporterDirective(Directive):
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    has_content = False
    option_spec = {
        'series-abbreviation': directives.unchanged,
        'dates': directives.unchanged,
        'neutral': directives.unchanged,
        'confirmed': directives.unchanged
    }

    def makeLabelNode(self,val,key=None,nodeType=value):
        node = nodes.container()
        if key:
            key = "%s: " % key
            label_node = label(rawsource=key,text=key)
            node += label_node
        value_node = nodeType(rawsource=val,text=val)
        node += value_node
        return node

    def run (self):
        if not self.options.has_key('series-abbreviation'):
            error = self.state_machine.reporter.error(
                'Invalid context: missing series-abbreviation option in reporter directive',
                nodes.literal_block(self.block_text, self.block_text), line=self.lineno)
            return [error]
        if not self.options.has_key('dates'):
            error = self.state_machine.reporter.error(
                'Invalid context: missing dates in reporter directive',
                nodes.literal_block(self.block_text, self.block_text), line=self.lineno)
            return [error]
        m = re.match("^([0-9]{4})/[0-9]{1,2}/[0-9]{1,2}-(?:([0-9]{4})/[0-9]{1,2}/[0-9]{1,2}|(present))",self.options["dates"])
        if not m:
            error = self.state_machine.reporter.error(
                'Invalid context: misformatted dates range in reporter directive. Format must be YYYY/MM/DD-YYYY/MM/DD or YYYY/MM/DD-present',
                nodes.literal_block(self.block_text, self.block_text), line=self.lineno)
            return [error]
        else:
            startyear = m.group(1)
            if m.group(2):
                endyear = m.group(2)
            else:
                endyear = m.group(3)
        
        reporter_box_node = reporterbox()

        if self.options.has_key("neutral"):
            reporter_node = reporterneutral()
        else:
            reporter_node = reporter()

        reporter_name = self.arguments[0].replace("'",u"\u0027")
        reporter_name_node = reportername(rawsource=self.arguments[0],text=reporter_name)

        description_node = descriptionbox()

        abbrev = self.makeLabelNode(self.options["series-abbreviation"],key="Abbrev")
        start = self.makeLabelNode(startyear,key="From")
        end = self.makeLabelNode(endyear,key="To")
        if self.options.has_key("neutral"):
            neutral =  self.makeLabelNode("yes",key="Neutral",nodeType=valueneutral)
        else:
            neutral =  self.makeLabelNode("no",key="Neutral")
            
        if self.options.has_key("confirmed"):
            confirmed = self.makeLabelNode("yes",key="Confirmed")
        else:
            confirmed = self.makeLabelNode("no",key="Confirmed",nodeType=valueunconfirmed)

        description_node += abbrev
        description_node += start
        description_node += end
        description_node += neutral
        description_node += confirmed

        feature_node = featurebox()
        keys = FEATURES.local.required.keys()
        keys.sort()
        for feature in keys:
            feature_node += self.makeLabelNode(u"req\u0027d",key=feature)
            
        keys = FEATURES.local.optional.keys()
        keys.sort()
        for feature in keys:
            feature_node += self.makeLabelNode("optional",key=feature)

        reporter_node += reporter_name_node
        reporter_node += description_node
        reporter_node += feature_node
        reporter_box_node += reporter_node
        return [reporter_box_node]

class NotesDirective(Directive):
    required_arguments = 0
    optional_arguments = 0
    has_content = True
    def run (self):
        content = '\n'.join(self.content)
        node = notes(rawsource=content)
        self.state.nested_parse(self.content, self.content_offset,
                                node)
        return [node]

directives.register_directive('credits', CreditsDirective)
directives.register_directive('fields', FieldsDirective)
directives.register_directive('court', CourtDirective)
directives.register_directive('citation-group', CitationGroupDirective)
directives.register_directive('reporter', ReporterDirective)
directives.register_directive('notes', NotesDirective)


class WriterForLegalCitem(Writer):
    def __init__(self):
        Writer.__init__(self)
        self.translator_class = HTMLTranslatorForLegalCitem

writer = WriterForLegalCitem()

description = ('Generates a specificaltion document from reStructuredText '
               'source.  ' + default_description)

output = publish_cmdline(reader=None, reader_name="standalone", writer=writer,
    description=description)

#scriptpath = os.path.split(sys.argv[0])[0]
#rootpath = os.path.join(scriptpath,os.path.pardir)
#rootpath = os.path.abspath(rootpath)
#indexpath = os.path.join(rootpath,"public","index.html")
#open(indexpath,"w+").write(output)

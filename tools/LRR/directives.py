'''
   Directives and roles for Legal Resource Registry
'''

import re

from docutils import nodes, statemachine
from docutils.parsers.rst import directives, Directive
from paths import PathTool
from utils import Utils
from traveler import Traveler
from nodes import *

traveler = Traveler()

class JurisdictionDirective(Directive,PathTool):
    required_arguments = 1
    optional_arguments = 0
    has_content = False
    option_spec = {}

    def run (self):
        pth = self.courtPathFromJurisdiction(self.arguments[0])
        rawlines = ""
        ifh = open(pth)
        while 1:
            line = ifh.readline()
            if not line: break
            if nodes.whitespace_normalize_name(line).startswith(".. reporter-key::"):
                reporter_key = re.sub("\.\.\s+reporter-key::\s*","",line).strip()
                try:
                    pth = self.reporterPathFromJurisdiction(self.arguments[0],reporter_key)
                except reporterPathException as err:
                    print "ERROR: cannot fine reporter for %s + %s" % (err.jurisdiction,err.reporterKey)
                    sys.exit()
                newlines = open(pth).read()
                newlines = newlines.split("\n")
                for i in range(0,len(newlines),1):
                    newlines[i] = re.sub("^(\s*)(\.\.\s+reporter::.*)","\\1\\2\n\\1      :jurisdiction: %s" % self.arguments[0],newlines[i])
                    newlines[i] = "   " + newlines[i]
                newlines = "\n".join(newlines)
                rawlines += newlines
            else:
                rawlines += line
        tab_width = self.options.get(
            'tab-width', self.state.document.settings.tab_width)
        include_lines = statemachine.string2lines(rawlines, tab_width,
                                                  convert_whitespace=True)
        self.state_machine.insert_input(include_lines, pth)
        return []

class BubbleDirective(Directive):
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    has_content = False
    option_spec = {
        'url': directives.unchanged,
        'title_en': directives.unchanged
        }

    def run (self):
        if not self.arguments[0]:
            error = self.state_machine.reporter.error(
                'Invalid context: bubble directive must have argument text.',
                nodes.literal_block(self.block_text, self.block_text), line=self.lineno)
            return [error]
        if not self.options.has_key('url'):
            error = self.state_machine.reporter.error(
                'Invalid context: bubble directive must have url option.',
                nodes.literal_block(self.block_text, self.block_text), line=self.lineno)
            return [error]
        newnode = bubble()
        newnode["title"] = self.arguments[0]
        newnode["url"] = self.options["url"]
        if self.options.has_key("title_en"):
            newnode["title_en"] = self.options["title_en"]
        return [newnode]

class FieldsDirective(Directive):
    required_arguments = 0
    optional_arguments = 0
    has_content = True
    option_spec = {}

    def run (self):
        features = {}
        if not traveler.features.local:
            for line in self.content:
                m = re.match("^:([a-z][-a-z]+):\s+(default|auxiliary|required|optional)",line)
                if not m:
                    error = self.state_machine.reporter.error(
                        'Invalid context: syntax error in option to initial fields directive',
                        nodes.literal_block(self.block_text, self.block_text), line=self.lineno)
                    return [error]
                traveler.features.defaults[m.group(2)] = m.group(1)
                traveler.features.set_defaults()
        else:
            traveler.features.set_base()
            for line in self.content:
                m = re.match("^:([a-z][-a-z]+):\s+(required|optional)",line)
                if not m:
                    error = self.state_machine.reporter.error(
                        'Invalid context: syntax error in option to subsequent fields directive. Note that default and auxiliary cannot be used here.',
                        nodes.literal_block(self.block_text, self.block_text), line=self.lineno)
                    return [error]
                if not traveler.features.defaults.auxiliary.has_key(m.group(1)) and not traveler.features.defaults.optional.has_key(m.group(1))  and not traveler.features.defaults.default.has_key(m.group(1)):
                    error = self.state_machine.reporter.error(
                        'Invalid context: undefined field in subsequent fields directive. Only fields initially declared as default, optional or auxiliary may be declared. line=%s' % self.lineno,
                        nodes.literal_block(self.block_text, self.block_text), line=self.lineno)
                    return [error]
                traveler.features.local[m.group(2)] = m.group(1)
        return []

class VariationDirective(Directive):
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    has_content = False
    option_spec = {}

    def run (self):
        # XXX HOOK: variation directive
        if traveler.hook.variation:
            traveler.hook.variation(self.arguments[0])
        return []


class CourtDirective(Directive,Utils):
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    has_content = True
    option_spec = {
        'court-id': directives.unchanged,
        'url': directives.unchanged,
        'flp-key': directives.unchanged,
        'en': directives.unchanged
    }

    def run (self):
        if not self.options.has_key('court-id'):
            error = self.state_machine.reporter.error(
                'Invalid context: missing court-id option in court directive',
                nodes.literal_block(self.block_text, self.block_text), line=self.lineno)
            return [error]

        # XXX HOOK: court directive
        if traveler.hook.court:
            traveler.hook.court(self.options)

        court_id_node = self.makeContainer("court-id")
        court_id_bubble = courtbubble(rawsource=self.options['court-id'],text=self.options['court-id'])
        court_id_bubble["href"] = self.mkGitHubUrl(traveler.gitHubStub,"courts",self.options["court-id"])
        court_id_node += court_id_bubble
        court_node = court()

        court_text = nodes.inline(rawsource=self.arguments[0],text=self.arguments[0])
        court_text_wrapper = altwrapper()
        court_text_wrapper += court_text

        if self.options.has_key("en"):
            court_text_wrapper["title"] = self.options["en"]

        if self.options.has_key("url"):
            court_ref = nodes.reference(refuri=self.options["url"])
            court_link = octiconlink()
            court_ref += court_link
            court_ref += court_text_wrapper
            court_node += court_ref
        else:
            court_node += court_text_wrapper

        reporters_node = self.makeContainer("reporters")
        self.state.nested_parse(self.content, self.content_offset, reporters_node)

        return [court_node,court_id_node,reporters_node]

class ReporterDirective(Directive,Utils):
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    has_content = True
    option_spec = {
        'edition-abbreviation': directives.unchanged,
        'dates': directives.unchanged,
        'neutral': directives.unchanged,
        'confirmed': directives.unchanged,
        'flp-series-cite-type': directives.unchanged,
        'flp-common-abbreviation': directives.unchanged,
        'jurisdiction': directives.unchanged
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

    def makeMiniBubble(self,jurisdiction,abbrev):
        node = minibubble(rawsource=abbrev,text=abbrev)
        node["href"] =  self.mkGitHubUrl(traveler.gitHubStub,"reporters",jurisdiction + ";" + abbrev)
        return node

    def run (self):
        if not self.options.has_key('edition-abbreviation'):
            error = self.state_machine.reporter.error(
                'Invalid context: missing edition-abbreviation option in reporter directive',
                nodes.literal_block(self.block_text, self.block_text), line=self.lineno)
            return [error]
        if not self.options.has_key('dates'):
            error = self.state_machine.reporter.error(
                'Invalid context: missing dates in reporter directive',
                nodes.literal_block(self.block_text, self.block_text), line=self.lineno)
            return [error]
        m = re.match("^([0-9]{4})/([0-9]{1,2})/([0-9]{1,2})-(?:([0-9]{4})/([0-9]{1,2})/([0-9]{1,2})|(present))",self.options["dates"])
        if not m:
            error = self.state_machine.reporter.error(
                'Invalid context: misformatted dates range in reporter directive. Format must be YYYY/MM/DD-YYYY/MM/DD or YYYY/MM/DD-present',
                nodes.literal_block(self.block_text, self.block_text), line=self.lineno)
            return [error]

        startyearDisplay = m.group(1)
        startyear = m.group(1)
        startmonth = m.group(2)
        startday = m.group(3)
        if m.group(4):
            endyear = m.group(4)
            endyearDisplay = m.group(4)
            endmonth = m.group(5)
            endday = m.group(6)
        else:
            endyearDisplay = m.group(7)
            endyear = False
            endmonth = False
            endday = False

        ## Save segments as short names to avoid going crazy.

        if traveler.hook.reporter_start:
            traveler.hook.reporter_start(self.arguments[0],self.options)
        
        # That's everything but variations, which are handled by the directive.
        dummy = nodes.generated()
        self.state.nested_parse(self.content, self.content_offset,
                                dummy)

        if traveler.hook.reporter_end:
            traveler.hook.reporter_end(self.arguments[0],self.options)

        reporter_box_node = self.makeContainer("reporter-box", suffix="")

        if self.options.has_key("neutral"):
            reporter_node = self.makeContainer("reporter neutral")
        else:
            reporter_node = self.makeContainer("reporter")

        reporter_name = self.arguments[0].replace("'",u"\u0027")
        reporter_name_node = self.makeContainer("reporter-name", rawsource=self.arguments[0],text=reporter_name)

        description_node = self.makeContainer("description-box",suffix="")

        abbrev = self.makeMiniBubble(self.options["jurisdiction"],self.options["edition-abbreviation"])
        start = self.makeLabelNode(startyearDisplay,key="From")
        end = self.makeLabelNode(endyearDisplay,key="To")
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

        feature_node = self.makeContainer("feature-box",suffix="")
        keys = traveler.features.local.required.keys()
        keys.sort()
        for feature in keys:
            feature_node += self.makeLabelNode(u"req\u0027d",key=feature)
            
        keys = traveler.features.local.optional.keys()
        keys.sort()
        for feature in keys:
            feature_node += self.makeLabelNode("optional",key=feature)

        reporter_node += reporter_name_node
        reporter_node += description_node
        reporter_node += feature_node
        reporter_box_node += reporter_node
        return [reporter_box_node]


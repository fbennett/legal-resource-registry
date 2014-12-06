#!/usr/bin/python
#-*- encoding: utf-8 -*-
"""
A Docutils Publisher script for the Legal Resource Registry
"""

gitHubStub = "https://github.com/fbennett/legal-resource-registry/tree/master/data"

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
from docutils.writers.html4css1 import Writer, HTMLTranslator
from docutils.parsers.rst import Directive
from docutils.transforms import Transform

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
class courtbubble (nodes.Inline, nodes.TextElement): pass
class minibubble (nodes.TextElement): pass
class bubble (nodes.Inline, nodes.TextElement): pass
class label (nodes.Inline, nodes.TextElement): pass
class value (nodes.Inline, nodes.TextElement): pass
class valueunconfirmed (nodes.Inline, nodes.TextElement): pass
class valueneutral (nodes.Inline, nodes.TextElement): pass
class featurename (nodes.Inline, nodes.TextElement): pass
class octiconlink (nodes.Inline, nodes.TextElement): pass
class altwrapper (nodes.Inline, nodes.TextElement): pass
class titled_reference (nodes.reference): pass


class trans (nodes.Inline, nodes.TextElement): pass
def role_trans(name, rawtext, text, lineno, inliner,
            options={}, content=[]):
    newnode = trans(rawsource=rawtext, text=text)
    pending = nodes.pending(MoveTrans)
    inliner.document.document.note_pending(pending)
    newnode += pending
    newnode.setup_child(pending)
    return [newnode], []
roles.register_local_role("trans", role_trans)


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
reporters_json = {}
traveling_jurisdiction = [[]]
traveling_variations = [{}]
courts_map = {}

class reporterPathException(Exception):
    def __init__(self,jurisdiction,reporterKey):
        self.jurisdiction = jurisdiction
        self.reporterKey = reporterKey

class FeaturesController:
    def __init__(self):
        pass

    def reset(self):
        FEATURES.local = None

class MoveTrans(Transform):
    default_priority = 100

    def apply(self):

        # self.startnode is the pending marker
        # self.startnode.parent is the translation text
        # self.startnode.parent.parent is the enclosing node, whatever it is

        translation = self.startnode.parent.astext()
        empty = nodes.generated()
        self.startnode.parent.replace_self(empty)

        # Okay, so we want to add a wrapper around children,
        # and make the wrapper the new child of self.startnode.parent.parent

        altie = altwrapper()
        altie["title"] = translation
        for child in self.startnode.parent.parent.children:
            newchild = child.deepcopy()
            altie += newchild
            altie.setup_child(newchild)
        self.startnode.parent.parent.children = [altie]
        self.startnode.parent.parent.setup_child(altie)

class HTMLTranslatorForLegalCitem(HTMLTranslator):

    def __init__(self, document, **kwargs):
        HTMLTranslator.__init__(self, document, **kwargs)
        settings = self.settings
        #self.d_class = DocumentClass(settings.documentclass)

    def visit_titled_reference(self, node):
        if node.has_key('title'):
            title = ' title="%s"' % node["title"]
        else:
            title = ""
        self.body.append('<a class="reference external" href="%s"%s>' % (node['refuri'],title))

    def depart_titled_reference(self, node):
        self.body.append('</a>')



    def visit_bubble(self, node):
        if node.has_key('title_en'):
            title_en = ' title="%s"' % node["title_en"]
        else:
            title_en = ""
        self.body.append('<a class="reference external" href="%s"%s>%s' % (node['url'],title_en,node['title']))

    def depart_bubble(self, node):
        self.body.append('</a>\n')

    def visit_altwrapper(self, node):
        if node.has_key('title'):
            title = ' title="%s"' % node["title"]
        else:
            title = ""
        self.body.append('<span%s>' % title)

    def depart_altwrapper(self, node):
        self.body.append('</span>\n')

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

    def visit_courtbubble(self, node):
        self.body.append('<a class="bubble" href="%s">' % node["href"])

    def depart_courtbubble(self, node): 
        self.body.append('</a>')

    def visit_minibubble(self, node):
        self.body.append('<a class="bubble mini" href="%s">' % node["href"])

    def depart_minibubble(self, node): 
        self.body.append('</a>')

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

    def visit_octiconlink(self, node):
        self.body.append('<span class="octicon octicon-link">')

    def depart_octiconlink(self, node): 
        self.body.append('</span>')

class PathTool:
    
    def __init__(self):
        pass

    def courtPathFromJurisdiction(self,arg):
        pthlst = ["data","courts"]
        pthlst.extend(arg.split(";"))
        pthlst.append("index.txt")
        pth = os.path.join(*pthlst)
        return pth

    def reporterPathFromJurisdiction(self,jurisdiction,reporterKey):
        pthlst = ["data","reporters"]
        pthlst.extend(jurisdiction.split(";"))
        # Drill down
        for i in range(2,len(pthlst),1):
            pth = os.path.join(*pthlst[0:i+1])
            filepth = os.path.join(pth,reporterKey,"index.txt")
            if os.path.exists(filepth):
                return filepth
        raise reporterPathException(jurisdiction,reporterKey)

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

class GitHubUrl:
    def __init__(self):
        pass

    def mkGitHubUrl (self,segment,courtID):
        idlst = courtID.split(";")
        if segment == "reporters":
            reporterID = idlst[-1]
            for i in range(1,len(idlst)-1,1):
                trypth = os.path.join(*[pth,"data",segment] + idlst[0:i] + [reporterID,"index.txt"])
                if os.path.exists(trypth):
                    idlst = idlst[0:i] + [reporterID]
                    break
        return os.path.join(*[gitHubStub,segment] + idlst + ["index.txt"])



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

class VariationDirective(Directive):
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    has_content = False
    option_spec = {}

    def run (self):
        traveling_variations[0][self.arguments[0]] = True
        return []


class CourtDirective(Directive,GitHubUrl):
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

        traveling_jurisdiction[0] = self.options["court-id"]
        if self.options.has_key("flp-key"):
            courts_map[self.options["flp-key"]] = self.options["court-id"]

        court_id_node = courtid()
        court_id_bubble = courtbubble(rawsource=self.options['court-id'],text=self.options['court-id'])
        court_id_bubble["href"] = self.mkGitHubUrl("courts",self.options["court-id"])
        court_id_node += court_id_bubble
        court_node = court()
        court_text = nodes.inline(rawsource=self.arguments[0],text=self.arguments[0])
        if self.options.has_key("url"):
            court_ref = titled_reference(refuri=self.options["url"])
            if self.options.has_key("en"):
                court_ref["title"] = self.options["en"]
            court_link = octiconlink()
            court_ref += court_link
            court_ref += court_text
            court_node += court_ref
        else:
            court_node += court_text

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

class ReporterDirective(Directive,GitHubUrl):
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
        node["href"] =  self.mkGitHubUrl("reporters",jurisdiction + ";" + abbrev)
        return node

    def findReporterSeries(self,bundle,name):
        for series in bundle:
            if series["name"] == name:
                return series
        return False

    def run (self):
        global reporters_json
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

        if self.options.has_key("flp-common-abbreviation"):
            bundle_key = self.options["flp-common-abbreviation"]
            if not reporters_json.has_key(bundle_key):
                bundle = []
                reporters_json[self.options["flp-common-abbreviation"]] = bundle
            else:
                bundle = reporters_json[bundle_key]
            series_name = self.arguments[0]
            edition_key = self.options["edition-abbreviation"]
                
            series = self.findReporterSeries(bundle,series_name)
            if not series:
                series = {}
                series["cite_type"] = self.options["flp-series-cite-type"]
                series["editions"] = {}
                series["mlz_jurisdiction"] = []
                series["name"] = series_name
                series["variations"] = {}
                bundle.append(series)
            if not series["mlz_jurisdiction"].count(traveling_jurisdiction[0]):
                series["mlz_jurisdiction"].append(traveling_jurisdiction[0])
                series["mlz_jurisdiction"].sort()
            if endyear:
                end = "%02d-%02d-%02dT00:00:00" % (int(endyear),int(endmonth),int(endday))
            else:
                end = None
            series["editions"][edition_key] = {
                "end": end,
                "start": "%02d-%02d-%02dT00:00:00" % (int(startyear),int(startmonth),int(startday))
                }
    
            # That's everything but variations, which are handled by the directive.
            
            dummy = nodes.generated()
            self.state.nested_parse(self.content, self.content_offset,
                                    dummy)
            for key in traveling_variations[0].keys():
                traveling_variations[0][key] = edition_key
            series["variations"].update(traveling_variations[0])
            traveling_variations[0] = {}

        reporter_box_node = reporterbox()

        if self.options.has_key("neutral"):
            reporter_node = reporterneutral()
        else:
            reporter_node = reporter()

        reporter_name = self.arguments[0].replace("'",u"\u0027")
        reporter_name_node = reportername(rawsource=self.arguments[0],text=reporter_name)

        description_node = descriptionbox()

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

directives.register_directive('variation', VariationDirective)
directives.register_directive('jurisdiction', JurisdictionDirective)
directives.register_directive('fields', FieldsDirective)
directives.register_directive('court', CourtDirective)
directives.register_directive('citation-group', CitationGroupDirective)
directives.register_directive('reporter', ReporterDirective)
directives.register_directive('notes', NotesDirective)
directives.register_directive('bubble', BubbleDirective)


class WriterForLegalCitem(Writer):
    def __init__(self):
        Writer.__init__(self)
        self.translator_class = HTMLTranslatorForLegalCitem

#writer = WriterForLegalCitem()

#description = ('Generates a specificaltion document from reStructuredText '
#               'source.  ' + default_description)

#output = publish_cmdline(reader=None, reader_name="standalone", writer=writer,
#    description=description)

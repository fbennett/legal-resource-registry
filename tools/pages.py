#!/usr/bin/python

import re,sys,os,os.path,json

from docutils.core import publish_string
from docutils.parsers.rst import directives
from rst4legalResourceRegistry import WriterForLegalCitem, JurisdictionDirective, FieldsDirective, CourtDirective, CitationGroupDirective, ReporterDirective, NotesDirective, FEATURES, reporters_json, courts_map

directives.register_directive('jurisdiction', JurisdictionDirective)
directives.register_directive('fields', FieldsDirective)
directives.register_directive('court', CourtDirective)
directives.register_directive('citation-group', CitationGroupDirective)
directives.register_directive('reporter', ReporterDirective)
directives.register_directive('notes', NotesDirective)

pth = os.path.split(sys.argv[0])[0]
pth = os.path.join(pth,"..")
pth = os.path.abspath(pth)

class IndentSyntaxException:
    def __init__(self,lineno,offset):
        self.lineno = lineno
        self.offset = offset

class GeneralSyntaxException:
    def __init__(self,lineno):
        self.lineno = lineno

class LineInfo:
    def __init__(self,lineno,line):
        bubblePageRex = re.compile("^(\s*)([^\[;<]+)(?:\[([^;<]+)\])*\s*<([^ ]+)>$")
        detailsPageRex = re.compile("^(\s*)([^ ;]+;[^ ]+)\s*$")
        courtTitleRex = re.compile(".. court::\s+(.*)$")
        self.title = None
        self.title_en = None
        self.page_name = None
        self.line_type = None
        self.level = None

        m = bubblePageRex.match(line)
        if m:
            offset = len(m.group(1))
            self.line_type = "bubblePage"
            self.title = m.group(2)
            self.title_en = m.group(3)
            self.page_name = m.group(4)
        if not m:
            m = detailsPageRex.match(line)
            if m:
                offset = len(m.group(1))
                self.line_type = "detailsPage"
                self.page_name = m.group(2)
                mypath = os.path.join(*[pth, "data","courts"] + self.page_name.split(";") + ["index.txt"])
                ifh = open(mypath)
                while 1:
                    line = ifh.readline()
                    if not line: break
                    m = courtTitleRex.match(line)
                    if m:
                        self.title = m.group(1).rstrip()
                        break
                ifh.close()

        if self.line_type:
            if offset % 4:
                raise IndentSyntaxException(lineno,offset)
            self.level = offset/4
                
class jurisdictionStack:
    def __init__(self):
        self.stack = []
        self.parent = None
        self.current = None

    def setLevelForPage(self,level,page_name):
        self.stack = self.stack[0:level]
        self.parent = os.path.join(*self.stack + ["index.html"])
        page_name = page_name.replace(";", "-")
        self.stack.append(page_name)
        self.current = os.path.join(*self.stack + ["index.html"])
        self.current_url = os.path.join(*self.stack[len(self.stack)-1:len(self.stack)] + ["index.html"])
        self.backtrack_path = os.path.join(*[".."] * len(self.stack))

class PageSource:
    def __init__(self):
        self.title = None
        self.title_en = None
        self.rst = ""

    def setTopmatter(self):
        self.rst += ".. include:: %s\n\n" % os.path.join(pth,"doc-src","fields.rst")
        self.rst += ".. include:: %s\n\n" % os.path.join(pth,"doc-src","banner.rst")

    def setTitle(self,title,title_en=None,char="-"):
        if title_en:
            # XXX This will require a transform in rst4legalResourceRegistry.py
            # print title_en
            pass
        self.title = title
        line = char * len(title)
        self.rst += "%s\n%s\n%s\n" % (line,title,line)

    def setDraft(self):
        self.rst += "\n.. include:: %s\n" % os.path.join(pth,"doc-src","draft-note.rst")
        
    def setCredits(self):
        self.rst += "\n.. include:: %s\n" % os.path.join(pth,"doc-src","credits.rst")
        
    def setBackref(self,backtrack,url):
        tmpl = "\n.. container:: back-button %s\n\n   .. image:: %s/graphics/circle-arrow-down-white.png\n      :target: %s\n\n"
        self.rst += tmpl % ("right",backtrack,url)
        self.rst += tmpl % ("left",backtrack,url)

    def setBubbles(self):
        self.rst += "\n.. container:: bubbles\n\n"

    def addBubble(self,title,current):
        self.rst += "   `%s <%s>`_\n" % (title,current)

    def setJurisdiction(self,page_name):
        self.rst += "\n.. jurisdiction:: %s" % page_name


class PageEngine:
    def __init__(self):
        specpth = os.path.join(pth,"doc-src","pages.txt")
        self.input = open(specpth)
        self.source = {}

    def getSpec(self):
        self.stack = jurisdictionStack()
        lineno = 0
        while 1:
            line = self.input.readline()
            if not line: break
            line = line.rstrip()
            lineno += 1
            lineInfo = LineInfo(lineno,line)
            if lineInfo.line_type == "bubblePage":
                self.stack.setLevelForPage(lineInfo.level,lineInfo.page_name)
                if not self.source.has_key(self.stack.current):
                    self.source[self.stack.current] = PageSource()
                    self.source[self.stack.current].setTopmatter()
                    self.source[self.stack.current].setTitle(lineInfo.title,title_en=lineInfo.title_en)
                    self.source[self.stack.current].setDraft()
                    self.source[self.stack.current].setCredits()
                    self.source[self.stack.current].setBackref(self.stack.backtrack_path,"../index.html")
                    self.source[self.stack.current].setBubbles()
                if lineInfo.level:
                    self.source[self.stack.parent].addBubble(lineInfo.title,self.stack.current_url)
            elif lineInfo.line_type == "detailsPage":
                self.stack.setLevelForPage(lineInfo.level,lineInfo.page_name)
                self.source[self.stack.parent].addBubble(lineInfo.title,self.stack.current_url)
                if not self.source.has_key(self.stack.current):
                    self.source[self.stack.current] = PageSource()
                    self.source[self.stack.current].setTopmatter()
                    self.source[self.stack.current].setTitle(self.source[self.stack.parent].title,title_en=self.source[self.stack.parent].title_en)
                    self.source[self.stack.current].setDraft()
                    self.source[self.stack.current].setCredits()
                    self.source[self.stack.current].setBackref(self.stack.backtrack_path,"../index.html")
                    self.source[self.stack.current].setJurisdiction(lineInfo.page_name)
            elif not line:
                continue
            else:
                raise GeneralSyntaxException(lineno)
        self.input.close()

    def publishPage(self,key,src):
        pubpath = os.path.join(pth,"public",key)
        try:
            os.makedirs(os.path.split(pubpath)[0])
        except:
            pass
        FEATURES.local = None
        writer = WriterForLegalCitem()
        keylst = key.split("/")
        upset = [".."] * (len(keylst)-1)
        css = os.path.sep.join(upset + ["legalcitem.css"])
        octicons = os.path.sep.join(upset + ["bower_components/octicons/octicons/octicons.css"])
        
        options = {
            "stylesheet": octicons + "," + css,
            "stylesheet_path": None,
            "embed_stylesheet": False
            }
        html = publish_string(src, reader=None, reader_name="standalone", writer=writer, settings_overrides=options)
        open(pubpath,"w+").write(html)
        

    def dumpPages(self):
        indexpath = os.path.join(pth,"doc-src","index.rst")
        src = open(indexpath).read()
        pwd = os.getcwd()
        os.chdir(os.path.join(pth,"doc-src"))
        self.publishPage("index.html",src)
        os.chdir(pwd)
        for key in self.source.keys():
            sys.stdout.write(".")
            sys.stdout.flush()
            self.publishPage(key,self.source[key].rst)
        sys.stdout.write("\n")
        sys.stdout.flush()

pageEngine = PageEngine()
try:
    pageEngine.getSpec()
except IndentSyntaxException as err:
    print "Error in pages.txt: offset of %d at line number %d is not a multiple of four." % (err.offset,err.lineno)
except GeneralSyntaxException as err:
    print "Error in pages.txt: unable to parse entry at line %d." % (err.lineno)

pageEngine.dumpPages()

def sortrep(a,b):
    if a["name"] > b["name"]:
        return 1
    elif a["name"] < b["name"]:
        return -1
    else:
        return 0

for key in reporters_json.keys():
    bundle = reporters_json[key]
    bundle.sort(sortrep)
    for series in bundle:
        series["mlz_jurisdiction"].sort()

open("reporters-new.json","w+").write(json.dumps(reporters_json,indent=2,sort_keys=True))
open("courts-map-flp.json","w+").write(json.dumps(courts_map,indent=2,sort_keys=True))

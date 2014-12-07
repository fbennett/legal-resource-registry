#!/usr/bin/python

import re,sys,os,os.path,json

from docutils.core import publish_string
from rst4legalResourceRegistry import WriterForLegalCitem, traveler
from LRR import traveler, Utils

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
        courtTitleRex = re.compile("^\.\. court::\s+(.*)$")
        courtTranslationRex = re.compile("^   :en:\s+(.*)$")
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
                    if not self.title:
                        m = courtTitleRex.match(line)
                        if m:
                            self.title = m.group(1).rstrip()
                    if self.title and not self.title_en:
                        m = courtTranslationRex.match(line)
                        if m:
                            self.title_en = m.group(1).strip()
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
    def __init__(self, jurisdiction):
        self.title = None
        self.title_en = None
        self.rst = ""
        if jurisdiction:
            self.processMe = False
        else:
            self.processMe = True

    def setTopmatter(self):
        self.rst += ".. include:: %s\n\n" % os.path.join(pth,"doc-src","fields.rst")
        self.rst += ".. include:: %s\n\n" % os.path.join(pth,"doc-src","banner.rst")

    def setTitle(self,title,title_en=None,char="-"):
        self.title = title
        if title_en:
            title = title + " :trans:`" + title_en + "`"
        else:
            pass
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

    def addBubble(self,title,current,title_en=None):
        if title_en:
            self.rst += "   .. bubble:: %s\n      :url: %s\n      :title_en: %s\n" % (title,current,title_en)
        else:
            self.rst += "   .. bubble:: %s\n      :url: %s\n" % (title,current)


    def setJurisdiction(self,page_name):
        self.rst += "\n.. jurisdiction:: %s" % page_name


class PageEngine(Utils):
    def __init__(self, writePages=False, jurisdiction=None, condition=None):
        specpth = os.path.join(pth,"doc-src","pages.txt")
        self.input = open(specpth)
        self.source = {}
        self.writePages = writePages
        self.jurisdiction = jurisdiction
        self.condition = condition

    def hasCurrent(self):
        return self.source.has_key(self.stack.current)

    def initPageSource(self):
        self.source[self.stack.current] = PageSource(self.jurisdiction)

    def current(self):
        return self.source[self.stack.current]

    def parent(self):
        return self.source[self.stack.parent]

    def checkReporters(self, pth, page_name):
        ifh = open(pth)
        while True:
            lline = ifh.readline()
            if not lline: break
            m = re.match("\s*\.\. reporter-key::\s+(.*)", lline)
            if m:
                pth = self.reporterPathFromJurisdiction(traveler.rootPath, page_name, m.group(1))
                txt = open(pth).read()
                if self.checkCondition(traveler, txt):
                    ifh.close()
                    return True
        ifh.close()
        return False
        # Get court page
        # Get reporter
        # Evaluate condition

    def getSpec(self):
        self.stack = jurisdictionStack()
        lineno = 0
        # XXX The stack reflects the full
        # XXX hierarchy to the top. Each stack slice gives
        # XXX us a source address, and we can set the rendering
        # XXX toggle there. It's a bit jury-rigged from an OO
        # XXX perspective, but it works.
        while 1:
            line = self.input.readline()
            if not line: break
            line = line.rstrip()
            lineno += 1
            lineInfo = LineInfo(lineno,line)

            self.stack.setLevelForPage(lineInfo.level,lineInfo.page_name)

            if lineInfo.line_type == "bubblePage":
                if not self.hasCurrent():
                    self.initPageSource()
                    self.current().setTopmatter()
                    self.current().setTitle(lineInfo.title,title_en=lineInfo.title_en)
                    self.current().setDraft()
                    self.current().setCredits()
                    self.current().setBackref(self.stack.backtrack_path,"../index.html")
                    self.current().setBubbles()
                if lineInfo.level:
                    self.parent().addBubble(lineInfo.title,self.stack.current_url,title_en=lineInfo.title_en)
            elif lineInfo.line_type == "detailsPage":

                self.parent().addBubble(lineInfo.title,self.stack.current_url,title_en=lineInfo.title_en)

                if not self.hasCurrent():
                    self.initPageSource()
                    if not self.condition:
                        self.current().setTopmatter()
                        self.current().setTitle(self.parent().title,title_en=self.parent().title_en)
                        self.current().setDraft()
                        self.current().setCredits()
                        self.current().setBackref(self.stack.backtrack_path,"../index.html")
                    self.current().setJurisdiction(lineInfo.page_name)
                    if self.jurisdiction:
                        self.checkJurisdiction(lineInfo.page_name)

                    # When a condition is imposed, append page content to single-page source string.
                    if self.condition:
                        pth = self.courtPathFromJurisdiction(traveler.rootPath, lineInfo.page_name)
                        if self.checkReporters(pth, lineInfo.page_name):
                            traveler.hook.data.single_page += self.current().rst + "\n\n"

            elif not line:
                continue
            else:
                raise GeneralSyntaxException(lineno)
        self.input.close()

    def checkJurisdiction(self, jurisdiction):
        if jurisdiction[0:len(self.jurisdiction)] == self.jurisdiction:
            for i in range(1,len(self.stack.stack)+1,1):
                key = os.path.join(*self.stack.stack[0:i] + ["index.html"])
                self.source[key].processMe = True
        

    def publishPage(self,key,src):
        pubpath = os.path.join(pth,"public",key)
        try:
            os.makedirs(os.path.split(pubpath)[0])
        except:
            pass
        # Soft reset
        traveler.features.reset()
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
        html = publish_string(src, reader=None, reader_name='standalone', writer=writer, settings_overrides=options)
        if self.writePages:
            open(pubpath,"w+").write(html)
        

    def dumpPages(self):
        indexpath = os.path.join(pth,"doc-src","index.rst")
        src = open(indexpath).read()
        pwd = os.getcwd()
        os.chdir(os.path.join(pth,"doc-src"))
        self.publishPage("index.html",src)
        os.chdir(pwd)
        if self.condition:
            self.publishPage(traveler.hook.opt.pagename,traveler.hook.data.single_page)
            return
        for key in self.source.keys():
            if not self.source[key].processMe:
                continue
            if self.writePages:
                sys.stdout.write("+")
            else:
                sys.stdout.write("-")
            sys.stdout.flush()
            self.publishPage(key,self.source[key].rst)
        sys.stdout.write("\n")
        sys.stdout.flush()

if __name__ == "__main__":

    from ConfigParser import ConfigParser
    from optparse import OptionParser

    os.environ['LANG'] = "en_US.UTF-8"

    usage = '\n%prog [option]'

    description="Render website and export from Legal Resource Registry."

    parser = OptionParser(usage=usage,description=description,epilog="Happy hacking!")
    parser.add_option("-P", "--plugin", dest="plugin",
                      default=None,
                      help='Process data using PLUGIN module.')
    parser.add_option("-w", "--write-pages", dest="writePages",
                      default=False,
                      action="store_true",
                      help='Write page ouput (default is False).')
    parser.add_option("-j", "--jurisdiction", dest="jurisdiction",
                      default=None,
                      help='Limit processing to specified jurisdiction.')

    (opt, args) = parser.parse_args()

    if len(args):
        print "This script accepts only a single option: --plugin"
        sys.exit()

    if opt.plugin:
        traveler.setHook(opt.plugin)

    jurisdiction = opt.jurisdiction
    if jurisdiction == None:
        jurisdiction = traveler.hook.opt.jurisdiction

    condition = None
    if traveler.hook.opt.condition:
        condition = traveler.hook.opt.condition

    pageEngine = PageEngine(writePages=opt.writePages, jurisdiction=jurisdiction, condition=condition)
    try:
        pageEngine.getSpec()
    except IndentSyntaxException as err:
        print "Error in pages.txt: offset of %d at line number %d is not a multiple of four." % (err.offset,err.lineno)
    except GeneralSyntaxException as err:
        print "Error in pages.txt: unable to parse entry at line %d." % (err.lineno)
        
    pageEngine.dumpPages()

    if traveler.hook.export:
        traveler.hook.export()

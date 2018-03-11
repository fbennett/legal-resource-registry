#!/usr/bin/python
#-*- encoding: utf-8 -*-

import re,sys,os,os.path,json

reload(sys)
sys.setdefaultencoding('utf8')

from docutils.core import publish_string
from docutils.writers.html4css1 import Writer
from rst4legalResourceRegistry import traveler
from LRR import traveler, Utils, LRRWorkbook, HTMLTranslatorForLegalResourceRegistry
import codecs

scriptpath = os.path.dirname(sys.argv[0])
rootpath = os.path.join(scriptpath, os.path.pardir)
scriptpath = os.path.abspath(scriptpath)
rootpath = os.path.abspath(rootpath)

#sys.path = [os.path.join(scriptpath, 'plugins')] + sys.path
#sys.path = [os.path.join(scriptpath, 'LRR')] + sys.path

countryNames = json.loads(codecs.open("tools/country-names.json", "r", "utf-8").read())


def countrySort(a, b):
    if a['countryName'] > b['countryName']:
        return 1
    elif a['countryName'] < b['countryName']:
        return -1
    else:
        return 0

class PageInfo:
    def __init__(self, pages, key):
        self.rst = ''
        self.title = ''
        self.pages = pages
        self.key = key

    def setFields(self):
        self.rst += "\n.. include:: %s\n" % os.path.join(rootpath,"doc-src","fields.rst")

    def setBanner(self):
        self.rst += "\n.. include:: %s\n" % os.path.join(rootpath,"doc-src","banner.rst")

    def setBreadcrumb(self, title, level, title_en=None):
        if title_en:
            self.rst += '\n.. breadcrumb:: %s\n   :level: %s\n   :en: %s\n' % (title, level, title_en)
        else:
            self.rst += '\n.. breadcrumb:: %s\n   :level: %s\n' % (title, level)
            
    def setTitle(self,title,title_en=None,char="-", courtPage=False):
        self.title = title
        self.title_en = title_en
        if self.key.count(os.path.sep):
            keyLst = self.key.split(os.path.sep)[0:-1]
            if courtPage:
                levelLst = range(2,len(keyLst[0:-1])+2,1)
            else:
                levelLst = range(2,len(keyLst)+2,1)
            levelLst.reverse()
            for i in range(1,len(keyLst),1):
                levelKey = os.path.sep.join(keyLst[0:i] + ['index.html'])
                levelTitle = self.pages[levelKey].title
                levelTitle_en = self.pages[levelKey].title_en
                if courtPage and i == (len(keyLst)-1):
                    title = self.pages[levelKey].title
                    title_en = self.pages[levelKey].title_en
                    break
                self.setBreadcrumb(levelTitle, levelLst[i], title_en=levelTitle_en)
        if title_en:
            title = title + " :trans:`" + title_en + "`"
        line = char * len(title) * 2
        self.rst += "\n%s\n%s\n%s\n" % (line,title,line)

    def setBubbles(self):
        self.rst += "\n.. container:: bubbles\n"

    def setBackref(self):
        tmpl = "\n.. container:: back-button %s\n\n   .. image:: %sgraphics/circle-arrow-down-white.png\n      :target: %s\n\n"
        backtrack = [".."] * len(self.key.split(os.path.sep)[0:-1])
        if backtrack:
            backtrack = os.path.join(*backtrack) + '/'
            url = '../index.html'
        else:
            backtrack = ''
            url = "index.html"
        self.rst += tmpl % ("right",backtrack,url)
        self.rst += tmpl % ("left",backtrack,url)

    def addBubble(self,title,current,title_en=None, cls=None):
        if title_en:
            title_en = '\n      :title_en: %s' % title_en
        else:
            title_en = ''
        if cls:
            cls = '\n      :class: %s' % cls
        else:
            cls = ''
        self.rst += "\n   .. bubble:: %s\n      :url: %s%s%s\n" % (title,current,title_en,cls)

    def setJurisdiction(self):
        jurisdiction = ':'.join(self.key.split(os.path.sep)[0:-1])
        self.rst += "\n.. jurisdiction:: %s" % jurisdiction

class SourceWalker(Utils):
    def __init__(self, writePages=False, writeSpreadsheets=False, jurisdiction=None):
        self.writePages = writePages
        self.writeSpreadsheets = writeSpreadsheets
        if jurisdiction:
            self.jurisdiction = jurisdiction.split(',')
        else:
            self.jurisdiction = None

        self.pages = {}
        self.addTopPages()

        # If a page of conditional returns is set, initialize the page
        if traveler.hook.opt.conditional:
            self.newPage(traveler.hook.opt.conditional["pageKey"], title=traveler.hook.opt.conditional["title"], courtPage=True)

        self.workbook = None
        self.workbook_urn = None

    def addTabs(self, rstSrc, tabName, level=0):
        tabs = [
            ["home", "Home"],
            ["index", "Jurisdictions"],
            ["contributors", "Updating a Jurisdiction"],
            ["developers", "Developers"]
            ]
        tabSrc = '\n.. container:: tabs\n'
        for tab in tabs:
            tabZero = '/'.join((['..'] * level) + [tab[0]])
            if tab[0] == tabName:
                tabSrc += '\n   .. tab:: %s\n      :url: %s.html\n      :selected:\n' % (tab[1], tabZero)
            else:
                tabSrc += '\n   .. tab:: %s\n      :url: %s.html\n' % (tab[1], tabZero)
        rstSrc = tabSrc + '\n' + rstSrc
        return rstSrc

    def addTopPages(self):
        for fileName in ["home", "index", "contributors", "developers"]:
            filePath = os.path.join(rootpath,"doc-src","%s.rst" % fileName)
            fileSrc = codecs.open(filePath, "r", "utf-8").read()
            fileSrc = '\n.. raw:: html\n\n   <div class="larger">\n\n' + fileSrc
            fileSrc = self.addTabs(fileSrc, fileName)
            self.newPage("%s.html" % fileName, rstSrc=fileSrc)

    def isJurisdictionOrParent(self, key):
        if not self.jurisdiction:
            return True
        keyLst = key.split('/')[0:-1]
        for jurisdiction in self.jurisdiction:
            jurisdictionLst = jurisdiction.replace(';', '/').replace(':', '/').split('/')
            keyLst = keyLst[0:len(jurisdictionLst)]
            jurisdictionLst = jurisdictionLst[0:len(keyLst)]
            if '/'.join(keyLst) == '/'.join(jurisdictionLst):
                return True
        return False
    
    def checkReporters(self, pth, page_name):
        ifh = codes.open(pth, "r", "utf-8")
        while True:
            lline = ifh.readline()
            if not lline: break
            m = re.match("\s*\.\. reporter-key::\s+(.*)", lline)
            if m:
                pth = self.reporterPathFromJurisdiction(traveler.rootPath, page_name, m.group(1))
                txt = codecs.open(pth, "r", "utf-8").read()
                if self.checkCondition(traveler, txt):
                    ifh.close()
                    return True
        ifh.close()
        return False

    def newPage(self, key, title=None, title_en=None, courtPage=False, rstSrc=None):
        if not self.pages.has_key(key):
            self.pages[key] = PageInfo(self.pages, key)
            if courtPage:
                self.pages[key].setFields()
            self.pages[key].setBanner()
            # Top pages (have rstSrc)
            # Category page (no rstSrc, no courtPage)
            # Details page (no rstSrc, but courtPage)
            if rstSrc:
                self.pages[key].rst += rstSrc
                #print self.pages[key].rst
            else:
                level = len(key.split('/')[0:-1])
                tabSrc = self.addTabs('', "index", level=level)
                self.pages[key].rst += tabSrc
                if key.count(os.path.sep) or traveler.hook.opt.conditional:
                    self.pages[key].setTitle(title, title_en=title_en, char="^", courtPage=courtPage)
                    self.pages[key].setBackref()
                if not traveler.hook.opt.conditional:
                    if courtPage:
                        self.pages[key].setJurisdiction()
                    else:
                        self.pages[key].setBubbles()

    def _walk(self, id):
        self.path = os.path.join(rootpath, "data/courts", os.path.sep.join(self.splitUrn(id)))
        self.stubLen = len(self.path.split(os.path.sep))

        for dirpath,dirnames,filenames in os.walk(self.path):

            urnLex = self.joinUrn(dirpath.split(os.path.sep)[self.stubLen-1:])

            if self.jurisdiction and len(urnLex.split(":")) == 1 and urnLex.split(":")[0] not in self.jurisdiction:
                for dirname in range(len(dirnames)-1,-1,-1):
                    dirnames.pop()

            if not self.isJurisdictionOrParent(urnLex.replace(":", "/").replace(';', "/")):
                continue

            if self.workbook and not urnLex.startswith(self.workbook_urn):
                self.workbook.close()
                self.workbook = None

            def sortCourtsFirst(a, b):
                aIsCourt = re.match("(?m)^\.\. court::", codecs.open(os.path.join(dirpath, a, "index.txt"), "r", "utf-8").read())
                bIsCourt = re.match("(?m)^\.\. court::", codecs.open(os.path.join(dirpath, b, "index.txt"), "r", "utf-8").read())
                am = re.match(".*?([0-9]+)$", a)
                if (aIsCourt and not bIsCourt) or a == "zhong.yuan" or a == "supreme.court":
                    a = "0" + a
                elif len(a) == 1 or am:
                    if am and len(am.group(1)) == 1:
                        a = re.sub("(.*?)([0-9])$", "\10\2", a)
                    a = "1"+a
                else:
                    a = "2" + a
                bm = re.match(".*?([0-9]+)$", b)
                if (bIsCourt and not aIsCourt) or b == "zhong.yuan" or a == "supreme.court":
                    b = "0" + b
                elif  len(b) == 1 or bm:
                    if bm and len(bm.group(1)) == 1:
                        b = re.sub("(.*?)([0-9])$", "\10\2", b)
                    b = "1"+b
                else:
                    b = "2" + b
                if a > b:
                    return 1
                elif a < b:
                    return -1
                else:
                    return 0

            dirnames.sort(sortCourtsFirst)

            thisKey = os.path.sep.join((dirpath.split(os.path.sep) + ['index.html'])[self.stubLen-1:])
            parentKey = os.path.sep.join((os.path.split(dirpath)[0].split(os.path.sep) + ['index.html'])[self.stubLen-1:])

            fh = codecs.open(os.path.join(dirpath, "index.txt"), "r", "utf-8")
            bubbleData = {
                "title": None,
                "en": None,
                "url": None,
                "unconfirmed": False
                }
            courtPage = False
            setForm = False
            while 1:
                line = fh.readline()
                if not line: break
                line = line.rstrip()

                if line.startswith('.. category:: '):
                    bubbleData["title"] = re.sub("\.\. category::\s+", "", line)
                    
                    # Klutzy. Spoofing a directive. Ugh.
                    if hasattr(traveler.hook, "category"):
                        categoryID = re.sub("^.*/data/courts/", "", dirpath).replace("/", ":")
                        options = { "category-id": categoryID }
                        traveler.hook.category(options, bubbleData["title"])

                elif line.startswith('.. court:: '):
                    bubbleData["title"] = re.sub("\.\. court::\s+", "", line)
                    courtPage = True
                elif line.startswith('   :en: '):
                    bubbleData["en"] = re.sub("   :en:\s+", "", line)
                elif line.startswith('   :url: '):
                    bubbleData["url"] = re.sub("   :url:\s+", "", line)
                elif line.startswith('   :unconfirmed:'):
                    bubbleData["unconfirmed"] = True
                elif line.find(':set-form:') > -1:
                    setForm = True
                    fileName = thisKey.split('/')[0:-1]
                    for i in range(0,len(fileName),1):
                        fileName[i] = fileName[i].upper()
                    countryTopCode = fileName[0]
                    countryCode = '-'.join(fileName)
                    if self.writeSpreadsheets:
                        fileName = "public/proofs-by-excel/%s" % countryCode
                        # We memo the urnLex key, and do the close (and zero out
                        # the workbook) when we move out of scope. Above -- so that we can clear
                        # and reset in one operation.
                        self.workbook = LRRWorkbook(fileName, countryCode, bubbleData['title'])
                        self.workbook_urn = urnLex
                        self.workbook_headings = {}
                    if countryNames.has_key(countryCode):
                        countryNames.pop(countryCode)
                    if countryNames.has_key(countryTopCode):
                        countryNames.pop(countryTopCode)

            # pageName is used in several branches below.
            # I know. Spaghetti. It works.
            pageName = dirpath.split(os.path.sep)[-1]
            pageName = "%s/index.html" % pageName

            # When a condition is imposed, append page content to single-page source string.
            if traveler.hook.opt.conditional and courtPage:
                courtPath = self.courtPathFromJurisdiction(traveler.rootPath, urnLex)
                if self.checkReporters(courtPath, urnLex):
                    self.pages[traveler.hook.opt.conditional["pageKey"]].rst += '\n.. jurisdiction:: %s\n' % urnLex
            else:
                self.newPage(thisKey, bubbleData['title'], title_en=bubbleData['en'], courtPage=courtPage)

            if setForm:
                fileName = urnLex.split(";")
                for i in range(0,len(fileName),1):
                    fileName[i] = fileName[i].upper()
                backtrack = ['..'] * len(fileName)
                fileName = "-".join(fileName)
                backtrack = "/".join(backtrack)
                self.pages[thisKey].addBubble('Data', "%s/proofs-by-excel/%s.xlsx" % (backtrack, fileName))

            if self.workbook:
                if courtPage:
                    headerLst = self.splitUrn(urnLex[len(self.workbook_urn):].strip(';'))
                    courtKey = headerLst[-1]
                    headerKey = self.joinUrn(headerLst[0:-1], isCourt)
                    if not headerKey:
                        headerKey = 'top'
                    headerData = self.workbook_headings[headerKey]
                    if not headerData.has_key('headerDone'):
                        if headerData['en']:
                            heading = '%s (%s) [%s]' % (headerData['title'],headerData['en'],headerKey)
                        else:
                            heading = '%s [%s]' % (headerData['title'],headerKey)
                        self.workbook.write_heading(heading)
                        headerData['headerDone'] = True
                    self.workbook.write_datarow(bubbleData['title'], courtKey, bubbleData['en'], None, bubbleData['url'])

                else:
                    headerKey = urnLex[len(self.workbook_urn):].strip(';')
                    if not headerKey:
                        headerKey = 'top'
                    self.workbook_headings[headerKey] = bubbleData

            if courtPage:
                cls = 'court'
            else:
                cls = ''

            if bubbleData["unconfirmed"]:
                cls += " unconfirmed"

            self.pages[parentKey].addBubble(bubbleData['title'], pageName, title_en=bubbleData['en'], cls=cls)

        if self.workbook:
            self.workbook.set_column_styles()
            self.workbook.set_column_widths()
            self.workbook.close()
            self.workbook = None

        return self.pages["index.html"].rst

    def walk(self):
        # So this will parse the config file and run walks in
        # sequence, passing the resulting top page to each in
        # turn.
        # Top page gets rendered last.
        fh = codecs.open(os.path.join(rootpath,"doc-src/pages.txt"), "r", "utf-8")
        rst = None
        while 1:
            line = fh.readline()
            if not line: break
            line = line.strip()
            self._walk(line)
        lst = []
        for fileName in os.listdir(os.path.join(rootpath, 'public/proofs-by-excel')):
            countryKey = fileName[:-5]
            if countryNames.has_key(countryKey):
                countryName = countryNames[countryKey]
                countryObj = {
                    "filePath": "proofs-by-excel/%s" % fileName,
                    "countryName": countryName
                    }
                lst.append(countryObj)
        lst.sort(countrySort)
        for countryObj in lst:
                self.pages['index.html'].addBubble(countryObj['countryName'], countryObj['filePath'])

    def publishPage(self,key):
        src = self.pages[key].rst
        pubpath = os.path.join(rootpath,"public",key)
        try:
            os.makedirs(os.path.split(pubpath)[0])
        except:
            pass
        # Soft reset
        traveler.features.reset()
        writer = Writer()
        writer.translator_class = HTMLTranslatorForLegalResourceRegistry
        keylst = key.split("/")
        upset = [".."] * (len(keylst)-1)
        css = os.path.sep.join(upset + ["screen.css"])
        octicons = os.path.sep.join(upset + ["bower_components/octicons/octicons/octicons.css"]) 
       
        options = {
            "stylesheet": octicons + "," + css,
            "stylesheet_path": None,
            "embed_stylesheet": False,
            "footnote_backlinks": True,
            "input_encoding": "utf-8"
            }
        src = src + '\n.. raw:: html\n\n   </div>\n'

        html = publish_string(src, reader=None, reader_name='standalone', writer=writer, settings_overrides=options)
        if self.writePages:
            codecs.open(pubpath, "w+", "utf-8").write(html)
        
    def dump(self):
        if traveler.hook.opt.conditional:
            if self.writePages:
                sys.stdout.write("+")
            else:
                sys.stdout.write("-")
            sys.stdout.write("\n")
            sys.stdout.flush()
            self.publishPage(traveler.hook.opt.conditional["pageKey"])
            return
        lst = []
        for key in self.pages.keys():
            if not self.isJurisdictionOrParent(key):
                continue
            if self.writePages:
                sys.stdout.write("+")
            else:
                sys.stdout.write("-")
            sys.stdout.flush()
            if self.pages[key].rst.strip().endswith(".. container:: bubbles"):
                self.pages[key].rst += '\n\n   [pending]\n'
            self.publishPage(key)
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
    parser.add_option("-s", "--write-spreadsheets", dest="writeSpreadsheets",
                      default=False,
                      action="store_true",
                      help='Write spreadsheet ouput (default is False).')
    parser.add_option("-j", "--jurisdiction", dest="jurisdiction",
                      default=None,
                      help='Limit processing to specified jurisdictions (comma-delimiter).')

    (opt, args) = parser.parse_args()

    if len(args):
        print "This script accepts only a single option: --plugin"
        sys.exit()

    if opt.plugin:
        traveler.setHook(opt.plugin)

    jurisdiction = opt.jurisdiction
    if jurisdiction == None:
        jurisdiction = traveler.hook.opt.jurisdiction

    walker = SourceWalker(writePages=opt.writePages, writeSpreadsheets=opt.writeSpreadsheets, jurisdiction=jurisdiction)
    walker.walk()
    walker.dump()

    if traveler.hook.export:
        traveler.hook.export()

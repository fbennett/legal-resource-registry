#!/usr/bin/python

from unidecode import unidecode
import os,sys,re
from urllib import URLopener
import urllib
import urllib2
from urllib2 import URLError
from lxml import etree
import json,tidy
import cStringIO

badHosts = {}

obj = {}

allHeadings = json.loads(open("HEADINGS.json").read())

html = open("PAGE-2.html").read()
indexDoc = etree.fromstring(html)
courtElems = indexDoc.xpath("//a[contains(@href,'/wlg/courts/nofr/')]")

urlh = URLopener()
siteRoot = "http://www.lexadin.nl"

def normalStr(str):
    if not str: return ""
    str = str.strip()
    str = re.sub("\n"," ",str)
    str = re.sub("\s+"," ",str)
    return str

def checkParent(e,tagname,boolean=False):
    parent = None
    for t in e.iterancestors():
        if t.tag == tagname:
            if boolean:
                parent = True
            else:
                parent = t
            break
    return parent

memoHeadings = {}

posCount = 0
for elem in courtElems:
    if not elem.text: continue
    country = normalStr(elem.text)
    if country == "Congo RDC": continue
    strIO = cStringIO.StringIO()
    urlStub = elem.attrib['href']
    if urlStub == '/wlg/courts/nofr/usstates/lxctusa.htm': continue
    if urlStub == '/wlg/courts/nofr/oeur/lxctjap.htm': continue

    print country

    countryHtml = urlh.open(siteRoot + urlStub).read()
    options = dict(output_xhtml=1, add_xml_decl=1, indent=1, tidy_mark=0)
    countryHtml = tidy.parseString(countryHtml,**options)
    countryHtml.write(strIO)
    strIO.seek(0)
    countryHtml = strIO.read()
    strIO.close()

    countryHtml = re.sub('xmlns="[^"]+"',"",countryHtml)
    countryDoc = etree.fromstring(countryHtml)
    courtHeadingElems = countryDoc.xpath("//font[@color='#009944']")
    for e in courtHeadingElems:
        heading = normalStr(e.text)
        #if not allHeadings.has_key(heading): 
        #    posCount += 1
        #    continue
        if not memoHeadings.has_key(heading):
            allHeadings[heading] = []
            memoHeadings[heading] = True
        print "  " + heading
        headingObj = {}
        headingObj["country"] = country
        headingObj["url"] = siteRoot + urlStub
        headingObj["segment"] = ""
        headingObj["courts"] = []
        
        # XXX Here we fetch out the court names for this segment only.
        # XXX Also the url to which each is linked, IF it does not return 404.
        # XXX Caste each as a separate object and append to list.
        # XXX Um ... and if only the first has no URL, we skip it.
        # posCount is our current position within the headers, in case that is helpful.
        parent = checkParent(e,"p")
        if not len(parent): continue

        terminate = False
        for sib in parent.itersiblings():
            if terminate:
                break
            boldAnchors = sib.xpath(".//a|.//b|.//font[@color='#009944']|.//br")
            for t in boldAnchors:
                if t.tag == "font":
                    terminate = True
                    break
                url = None
                if t.tag == "br" and checkParent(t,"b",boolean=True):
                    txt = normalStr(t.tail)
                elif t.tag == "a":
                    txt = normalStr(t.text)
                    if t.attrib.has_key("href"):
                        url = t.attrib["href"]
                elif t.tag == "b":
                    txt = normalStr(t.text)
                else:
                    continue
                if not txt: continue

                courtObj = {
                    "name": txt
                    }
                if url:
                    try:
                        host = urllib.splithost(re.sub("https?:","",url))[0]
                        if badHosts.has_key(host):
                            raise
                        response = urllib2.urlopen(url, None, 25)
                        if response.getcode() == 200:
                            courtObj["url"] = url
                    except URLError as err:
                        if type(err.reason) != type("str") and err.reason.errno == -2:
                            badHosts[host] = True
                    except:
                        #print "Failed URL: %s" % url
                        pass
                headingObj["courts"].append(courtObj)

                print "    %s" % (txt,)
                #print "      POW(2)"
                #break

        if not allHeadings.has_key(heading):
            allHeadings[heading] = []
        allHeadings[heading].append(headingObj)
        #print "  %s" % heading
    #if posCount == 1:
    #    sys.exit()
    posCount += 1

open("HEADINGS-new.json","w+").write(json.dumps(allHeadings,sort_keys=True,indent=2))

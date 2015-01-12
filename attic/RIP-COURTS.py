#!/usr/bin/python

comment = '''
  Several to-do things here.

  We need to stir in country codes. That should be the top-level
  key for each entry in the obj. -- HA! We can access the ISO 3166
  code via the country links. Super. [GOOD-ENOUGH DONE]

  We should maybe fetch the official languages of each jurisdiction.
  That will provide a hint as to whether English-language court names
  are sufficient. [GOOD-ENOUGH DONE]

  We need to follow out and get the top-level courts for countries
  that have no local court listed. These are mostly stated in free
  text in the country pages.

  We need to grab the foreign-language version of the name from
  the court page, where possible. This is tagged, so should be
  pretty reliable, for a first shot. [GOOD-ENOUGH DONE]

  We need a script to inject this data into the repo.

  We need a simple JS-driven filtering interface for the top page
  so that the data remains manageable. Hide all jurisdictions
  by default, and reveal Google-like, with "all" noted as a
  complete reveal.

  We need to provide for renaming court files based on changes to the
  court-id attribute during processing, to simplify maintenance.

  We need to finish the submission instructions.

  We need to contact Wikipedia and see about spreading the
  word.

  We need to liaise with Shima-san about contributing to the
  data set.
'''

import os,sys,re
from urllib import URLopener
from lxml import etree
import json



obj = {}

urlh = URLopener()

html = urlh.open("http://en.wikipedia.org/wiki/List_of_supreme_courts_by_country").read()

doc = etree.fromstring(html)

entries = doc.xpath("//table[@class='wikitable']//tr")

stops = ["the","of","a"]

def makeID(court):
    courtID = court.lower()
    courtID = re.split("\s+",courtID)
    for i in range(len(courtID)-1,-1,-1):
        word = courtID[i]
        if word in stops:
            courtID = courtID[0:i] + courtID[i+1:]
    return ".".join(courtID)

for entryNode in entries:
    countryNodes = entryNode.xpath("td[1]//a")
    if len(countryNodes):
         country = countryNodes[0].text

         print "Processing: %s" % country

         #if country != "Guinea": continue

         countryLink = countryNodes[0].attrib["href"][1:]
         
         countryHtml = urlh.open(os.path.join("http://en.wikipedia.org",countryLink)).read()
         countryDoc = etree.fromstring(countryHtml)

         # XXX Pretty-much good. Will need some error handling for some jurisdictions to get
         # XXX a full set of codes.
         countryObj = {
             "official-languages": [],
             "country-name": country,
             "courts": {}
             }
         countryCodes = countryDoc.xpath("//table//th[a[@href='/wiki/ISO_3166']]/following-sibling::td/a/text()")
         if len(countryCodes):
             countryCodeData = countryCodes[0]
             #print "  " + countryCodes[0]
             obj[countryCodeData] = countryObj
         else:
             print "WARNING: %s has no country code" % country
             obj[country] = countryObj
         
         # XXX Pretty-much good. Will need some touch-up for some of the European jurisdictions.
         countryLangs = countryDoc.xpath("//table//th[contains(text(),'Official language') or a[contains(text(),'Official language')] or b[contains(text(),'Official language')] or contains(text(),'National language') or a[contains(text(),'National language')] or b[contains(text(),'National language')]]/following-sibling::td")
         if len(countryLangs):
             for langNode in countryLangs:
                 nodes = langNode.xpath("*//a[not(ancestor::sup)]")
                 if len(nodes):
                     for node in nodes:
                         countryObj["official-languages"].append(etree.tostring(node, method="text", with_tail=False, encoding="unicode"))
                 else:
                     nodes = langNode.xpath("text()")
                     for node in nodes:
                         countryObj["official-languages"].append(node)
         else:
             print "WARNING: %s has no country langs" % country

         courtNodes = entryNode.xpath("td[2]//a")
         if len(courtNodes) == 1 and courtNodes[0].text == "International supreme courts":
             courtNodes.pop()
         if len(courtNodes):
             for courtNode in courtNodes:
                 if not courtNode.text: continue
                 countryID = makeID(country)
                 courtID = makeID(courtNode.text)
                 if courtID.endswith(countryID):
                     courtID = courtID[0:-1 * len(countryID) - 1]
                 courtLink = "http://en.wikipedia.org%s" % (courtNode.attrib["href"])
                 courtObj = {
                     "en": courtNode.text
                     }
                 countryObj["courts"][courtID] = courtObj
                 if not courtLink.find("redlink") > -1:
                     courtObj["url"] = courtLink
                     courtHtml = urlh.open(courtLink).read()
                     courtDoc = etree.fromstring(courtHtml)
                     langs = courtDoc.xpath("//a[contains(@href,'language')]/following-sibling::span[@lang][1]")
                     if len(langs):
                         courtObj["local"] = etree.tostring(langs[0], method="text", with_tail=False, encoding="unicode")
                         #print "  %s (1): %s" % (country,etree.tostring(langs[0], method="text", with_tail=False, encoding="unicode"))
                         #break
                     else:
                         nodes = courtDoc.xpath("//h2[span[@id='Judicial_branch']]/following-sibling::p")
                         if len(nodes) == 0:
                             nodes = courtDoc.xpath("//div[@id='mw-content-text']//p[not(ancestor::table)]")
                         if len(nodes):
                             node = nodes[0]
                             realname = node.xpath("i|b|a")
                             if len(realname) and realname[0].text:
                                 courtObj["local"] = etree.tostring(realname[0], method="text", with_tail=False, encoding="unicode")
                                 #print "  %s (2) %s" % (country,etree.tostring(realname[0], method="text", with_tail=False, encoding="unicode"))
                             else:
                                 paratext = etree.tostring(node, method="text", with_tail=False, encoding="unicode")
                                 m = re.match("(?sm).*?\s+(?:\"([^\"]+)\"|or\s+([^,\.]+)).*",paratext)
                                 if m:
                                     if m.group(1):
                                         courtObj["local"] = m.group(1)
                                         #print "  %s (3) %s" % (country,m.group(1))
                                     else:
                                         courtObj["local"] = m.group(2)
                                         #print "  %s (4) %s" % (country,m.group(2))
                 
         else:
             print "No court listed for: %s" % country

open("ALL-COURTS.json","w+").write(json.dumps(obj,indent=2))

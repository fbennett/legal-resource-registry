#!/usr/bin/python
#-*- encoding: utf-8 -*-

import urllib
from lxml import etree
import csv
from unidecode import unidecode
import re

ofh = open("MN.csv", "w+")
csvh = csv.writer(ofh)

csvh.writerow(['', '', '', '', '', '', ''])
csvh.writerow(['', '', '', '', '', '', ''])
csvh.writerow(['', 'Legal Resource Registry: Mongolia (MN)', '', '', '', '', ''])
csvh.writerow(['', '', '', '', '', '', ''])

csvh.writerow(['', 'Mongolia [top]', '', '', '', '', ''])

supct = u"Улсын дээд шүүх"
csvh.writerow(['', '', supct, unidecode(supct), "Supreme Court", ''])

conct = u"Улсын Үндсэн хуулийн цэц"
csvh.writerow(['', '', conct, unidecode(conct), "Constitutional Court", ''])

opener = urllib.URLopener()
ifh = opener.open("http://en.wikipedia.org/wiki/Provinces_of_Mongolia")
txt = ifh.read()
doc = etree.HTML(txt)

rows = doc.xpath("//h2[span[@id='List_of_Provinces']]/following-sibling::table[contains(@class,'wikitable')][1]/tr")

for i in range(1, len(rows), 1):
    row = rows[i]
    en = row.xpath('td[2]/a')[0].text
    mn = row.xpath("td[3]/span[@lang='mn']")[0].text
    roman = '.'.join(re.split("[- ]", unidecode(unicode(en)).lower()))
    csvh.writerow(['', '', '', '', '', '', ''])
    heading = '%s (%s) [%s]' % (mn, en, roman)
    csvh.writerow(['', heading, '', '', '', '', ''])

    mn = "Аймгийн шүүх"
    en = "Aimag Court"
    roman = "aimgiin.shuukh"

    csvh.writerow(['', '', mn, roman, en, '', ''])

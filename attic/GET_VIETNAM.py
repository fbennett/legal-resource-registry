#!/usr/bin/python
#-*- encoding: utf-8 -*-

import urllib
from lxml import etree
import csv
from unidecode import unidecode
import re

ofh = open("VN.csv", "w+")
csvh = csv.writer(ofh)

csvh.writerow(['', '', '', '', '', '', ''])
csvh.writerow(['', '', '', '', '', '', ''])
csvh.writerow(['', 'Legal Resource Registry: Viet Nam (VN)', '', '', '', '', ''])

opener = urllib.URLopener()

ifh = opener.open("http://en.wikipedia.org/wiki/List_of_districts_of_Vietnam")
txt = ifh.read()

doc = etree.HTML(txt)

provinces = doc.xpath("//h2/span[@class='mw-headline']/a")

def makeVariants(ptxt):
    ptxt = ptxt.strip()
    roman = re.split("[\-. ]", unidecode(unicode(ptxt)))
    for i in range(0, len(roman), 1):
        roman[i] = roman[i].lower()
    roman = u'.'.join(roman)
    en = unidecode(unicode(ptxt))
    en = en.replace("Toa an nhan dan", "People's Court")
    return [ptxt, roman, en]

def courtLine(place=None):
    lst = []
    if place:
        lst.append(place)
    lst.append(u"Tòa án nhân dân")
    ptxt = ' '.join(lst)
    return makeVariants(ptxt)


csvh.writerow(['', u"Viet Nam [top]", '', '', '', '', ''])
csvh.writerow(['', '', '', '', '', '', ''])

[ptxt, roman, en] = makeVariants(u"Tòa án Nhân dân Tối cao")
csvh.writerow(['', '', ptxt, roman, 'Supreme People\'s Court', '', 'http://www.toaan.gov.vn/'])


for province in provinces:
    ptxt = province.text.strip()

    ptxt = re.sub("\s+(City|Province)\s*$", "", ptxt)

    print ptxt

    [ptxt, roman, en] = makeVariants(ptxt)
    header = u"%s (%s) [%s]" % (ptxt, en, roman)
    province_roman = roman

    csvh.writerow(['', '', '', '', '', '', ''])
    csvh.writerow(['', header, '', '', '', '', ''])
    csvh.writerow(['', '', '', '', '', '', ''])
    
    [ptxt, roman, en] = courtLine()
    csvh.writerow(['', '', ptxt, roman, en, '', ''])

    parent = province.getparent().getparent()
    districts = parent.xpath("following-sibling::ul[1]/li/a")
    for district in districts:
        ptxt = district.text.strip()

        [ptxt, roman, en] = makeVariants(ptxt)
        roman = "%s;%s" % (province_roman, roman)
        header = u"%s (%s) [%s]" % (ptxt, en, roman)
        csvh.writerow(['', '', '', '', '', '', ''])
        csvh.writerow(['', header, '', '', '', '', ''])
        csvh.writerow(['', '', '', '', '', '', ''])

        [ptxt, roman, en] = courtLine()
        csvh.writerow(['', '', ptxt, roman, en, '', ''])

#!/usr/bin/python

import xlrd,os,sys,re,json
from unidecode import unidecode

def sortBySplitLength(a,b):
    a = len(a.split(';'))
    b = len(b.split(';'))
    if a > b:
        return 1
    elif a < b:
        return -1
    else:
        return 0

class LRRFileMaker:
    def __init__(self, fileName):
        self.fileName = fileName
        self.countryCode = ';'.join(fileName[:-5].lower().split('-'))
        self.category_obj = {}
        self.category_lst = []
        self.current = None

    def parseCourtRow(self, row):
        url = ''
        courtName = row[2]
        enName = row[4]
        if len(row) > 6:
            url = row[6]
        if not row[3]:
            roman = unidecode(row[2])
        else:
            roman = unidecode(row[3])
        roman = re.split("\s+", roman)
        for i in range(len(roman)-1,-1,-1):
            if ["for", "of", "the"].count(roman[i]):
                roman.pop(i)
        roman = " ".join(roman)
        roman = re.sub("[-/,:\s]+",".",roman.lower())
        courtID = re.sub("[,\'()]","", roman)
        court = {
            'type': 'detailsPage',
            'title': courtName,
            'en': enName,
            'url': url,
            'key': '%s;%s' % (self.current['key'], courtID)
            }
        # Set on "current" pointer object
        self.current['courts'].append(court)
        
    def parseCategoryRow(self, row):
        # Okay.
        # If this is "top" give it the country code.
        # Otherwise, prepend country code + ';'
        m = re.match('^([^\(]+)(?:\(([^\[]+)\))*\s*\[(.+)\]', row[1])
        if m:
            categoryInfo = {
                'type': 'categoryPage',
                'title': None,
                'key': None,
                'en': None,
                'courts': []
                }
            categoryInfo['title'] = m.group(1).strip()
            if m.group(2):
                categoryInfo['en'] = m.group(2).strip()
            key = m.group(3).strip()
            if key == 'top':
                key = self.countryCode
            else:
                key = '%s;%s' % (self.countryCode, key)
            categoryInfo['key'] = key
            # Set it as a key, and set global "current" pointer to it.
            self.category_lst.append(key)
            self.category_obj[key] = categoryInfo
            self.current = categoryInfo

    def makePathFromKey(self, key):
        pth = key.replace(';', os.path.sep)
        try:
            os.makedirs(pth)
        except:
            pass
        return os.path.join(pth, 'index.txt')

    def castCategory(self, key, setForm):
        obj = self.category_obj[key]
        rst = '.. category:: %s\n   :category-id: %s\n' % (obj['title'], obj['key'])
        if obj['en']:
            rst += '   :en: %s\n' % obj['en']
        if setForm:
            rst += '   :set-form:\n'
        filePath = self.makePathFromKey(key)
        open(filePath, 'w+').write(rst)

    def castCourt(self, court):
        rst = '.. court:: %s\n   :court-id: %s\n' % (court['title'], court['key'])
        if court['en']:
            rst += '   :en: %s\n' % court['en']
        if court['url']:
            rst += '   :url: %s\n' % court['url']
        filePath = self.makePathFromKey(court['key'])
        open(filePath, 'w+').write(rst)

    def process(self):
        wb = xlrd.open_workbook(self.fileName)
        ws = wb.sheet_by_index(0)
        for i in range(2,ws.nrows,1):
            row = ws.row_values(i)
            if not row[1] and row[2]:
                self.parseCourtRow(row)
            elif row[1] and row[2] == '':
                self.parseCategoryRow(row)
        # Sort the list by split length.
        self.category_lst.sort(sortBySplitLength)
        # Iterate over keys in list, creating subdirectories and writing files.
        for i in range(0, len(self.category_lst), 1):
            key = self.category_lst[i]
            if i == 0:
                setForm = True
            else:
                setForm = False
            self.castCategory(key, setForm)
            for court in self.category_obj[key]["courts"]:
                self.castCourt(court)

if __name__ == "__main__":

    from ConfigParser import ConfigParser
    from optparse import OptionParser

    os.environ['LANG'] = "en_US.UTF-8"

    usage = '\n%prog [option]'

    description="Cast a file hierarchy ready for the Legal Resource Registry."

    parser = OptionParser(usage=usage,description=description,epilog="Happy hacking!")
    parser.add_option("-f", "--file", dest="file",
                      default=None,
                      help='Process data contained in xls file FILE.')

    (opt, args) = parser.parse_args()

    if not opt.file:
        print '-f option is required'
        sys.exit()
    fileMaker = LRRFileMaker(opt.file)
    fileMaker.process()

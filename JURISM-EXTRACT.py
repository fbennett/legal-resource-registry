#!/usr/bin/python

import os,sys,re,json

TESTING = ['ca', 'un.int']

def sortInfo(a, b):
    if a[0] > b[0]:
        return -1
    elif a[0] < b[0]:
        return 1
    else:
        return 0
    
class Courts():

    def __init__(self, opt):
        self.opt = opt
        self.walk()

    def checkFile(self, dirname):
        ifh = open(os.path.join(dirname,'index.txt'))
        while 1:
            line = ifh.readline()
            if not line:
                ifh.close()
                break
            line = line.strip()
            m = re.match("^\.\.\s+category::\s*(.*)$",line)
            if m:
                name = m.group(1)
                ifh.close()
                return name
            m = re.match("^\.\.\s+court::", line)
            if m:
                ifh.close()
                return None
        ifh.close()
        raise
    
    def walk(self):
        for dirname,dirs,files in os.walk('./data/courts'):
            #if dirname == './data/courts': continue
            path = os.path.join('jurism','/'.join(dirname.split('/')[3:]))
            dlst = dirname.split(os.path.sep)
            key = dlst[-1]
            if self.opt.testing and len(dlst) > 3 and not dlst[3] in TESTING:
                continue
            name = self.checkFile(dirname)
            if name == None:
                continue
            # name (not needed)
            # key
            # path
            # immediate child key/name pairs
            # count
            childJurisdictions = []
            for i in range(len(dirs)-1,-1,-1):
                d = dirs[i]
                subname = self.checkFile(os.path.join(dirname,d))
                if subname == None:
                    dirs.pop(i)
                    continue
                hasChildren = 0
                for subchild in os.listdir(os.path.join(dirname,d)):
                    subchildPath = os.path.join(dirname,d,subchild)
                    if (os.path.isdir(subchildPath) and self.checkFile(subchildPath)):
                        hasChildren = 1
                        break
                childJurisdictions.append([d, subname, hasChildren])
            #if len(childJurisdictions) == 0:
            #    continue
        
            # Produce one file for each hit which
            # (1) is saved to the path
            # (2) is named by the single-element key
            # (3) contains the key, name and child count of each entry
            try:
                os.makedirs(path)
            except:
                pass
            # Sort in reverse order (for stable output - reverse-order sort
            # has not special significance)
            childJurisdictions.sort(sortInfo)
            open(os.path.join(path,'info.json'),'w+').write(json.dumps(childJurisdictions))
            sys.stdout.write('.')
            sys.stdout.flush()
        
        newCountries = json.loads(open('./tools/country-names.json').read())
        countries = json.loads(open('./jurism/info.json').read())
        oldCountries = {}
        for entry in countries:
            oldCountries[entry[0]] = True
        
        for key in newCountries:
            if not oldCountries.has_key(key.lower()):
                countries.append([key.lower(),newCountries[key],0])
        
        open('./jurism/info.json', 'w+').write(json.dumps(countries))


if __name__ == '__main__':
    from ConfigParser import ConfigParser
    from optparse import OptionParser

    os.environ['LANG'] = "en_US.UTF-8"

    usage = '\n%prog [options]'

    description="Writes minimal JSON expression of LRR jurisdiction data into source file."

    parser = OptionParser(usage=usage,description=description,epilog="And that's all for now!")
    parser.add_option("-t", "--t", dest="testing",
                      default=False,
                      action="store_true", 
                      help='Output minimal test data only.')

    (opt, args) = parser.parse_args()


    Courts(opt)

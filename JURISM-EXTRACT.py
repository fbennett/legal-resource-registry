#!/usr/bin/python

import os,sys,re,json

def checkFile(dirname):
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

def sortInfo(a, b):
    if a[0] > b[0]:
        return -1
    elif a[0] < b[0]:
        return 1
    else:
        return 0

for dirname,dirs,files in os.walk('./data/courts'):
    #if dirname == './data/courts': continue
    path = os.path.join('jurism','/'.join(dirname.split('/')[3:]))
    key = dirname.split('/')[-1]
    name = checkFile(dirname)
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
        subname = checkFile(os.path.join(dirname,d))
        if subname == None:
            dirs.pop(i)
            continue
        hasChildren = 0
        for subchild in os.listdir(os.path.join(dirname,d)):
            subchildPath = os.path.join(dirname,d,subchild)
            if (os.path.isdir(subchildPath) and checkFile(subchildPath)):
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

#!/usr/bin/python
#-*- encoding: utf-8 -*-

import re,os,sys,pinyin,shutil

top = 'data/courts/cn'

count = 0

def makeVariants(ptxt):
    ptxt = ptxt.strip()
    plst = list(ptxt)
    for i in range(0, len(plst), 1):
        plst[i] = pinyin.get(plst[i])
    roman = u'.'.join(plst)
    en = pinyin.get(ptxt)
    try:
        en = en[0].upper() + en[1:].lower()
    except:
        print ptxt
        print en
        raise
    return [ptxt, roman, en]

[courtName, courtKey, courtEn] = makeVariants(u'法院')
courtEn = 'District Court'

def pushDown(params):
    # Get the old path and the new path
    old_path = params['path']
    new_path = '/'.join(params['path'].split('/')[0:-1])
    # Create subdir
    subdir = os.path.join(new_path, params['placeKey'])
    if not os.path.exists(subdir):
        os.mkdir(subdir)
    # Write category details
    subdir_filepath = os.path.join(subdir, 'index.txt')
    fh = open(subdir_filepath, 'w+')
    fh.write(u'.. category:: %s\n' % params['placeName'])
    fh.write(u'   :category-id: blah\n')
    fh.write(u'   :en: %s\n' % params['placeEnglish'])
    fh.close()
    # Create subsubdir
    subsubdir = os.path.join(subdir, courtKey)
    if not os.path.exists(subsubdir):
        os.mkdir(subsubdir)
    # Write court details
    subsubdir_filepath = os.path.join(subsubdir, 'index.txt')
    fh = open(subsubdir_filepath, 'w+')
    fh.write(u'.. court:: %s\n' % courtName)
    fh.write(u'   :court-id: blah\n')
    fh.write(u'   :en: %s\n' % courtEn)
    fh.close()
    # Remove original court file and directory
    if os.path.exists(params['path']):
        shutil.rmtree(params['path'], ignore_errors=True)

for [dirname, dirs, files] in os.walk(top):
    for i in range(len(dirs)-1, -1, -1):
        d = dirs[i]
        #print "Inspecting: %s" % d
        if not len(os.listdir(os.path.join(dirname, d))):
            #print "REMOVING: %s" % os.path.join(dirname, d)
            os.rmdir(os.path.join(dirname, d))
            dirs.pop(i)
    for filename in files:
        fh = open(os.path.join(dirname, filename))
        while 1:
            line = fh.readline()
            if not line: break
            line = line.strip()
            line = line.decode('utf-8')
            params = {}
            if line.startswith(u'.. court::') and line.endswith(u'法院'):
                if line == u'.. court:: 最高人民法院': continue
                m = re.match(u'\.\. court::\s+(.*)法院.*', line)
                placeName = m.group(1)
                if not placeName: continue
                [ptxt, roman, en] = makeVariants(placeName)
                #print roman
                params['placeName'] = ptxt
                params['placeKey'] = roman
                params['placeEnglish'] = en
                params['path'] = dirname
                count += 1
                #print placeName
                pushDown(params)
                break
print count

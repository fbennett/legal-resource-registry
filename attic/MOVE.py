#!/usr/bin/python

import os,sys

if False:
    for stateCode in os.listdir('.'):
        if len(stateCode) != 2: continue
        for districtCode in os.listdir(stateCode):
            if districtCode == 'index.txt': continue
            if districtCode == 'district.court':
                #print "%s: %s" % (stateCode, districtCode)
                txt = open(os.path.join(stateCode, districtCode, 'index.txt')).read()
                newName = '%s.d' % stateCode
                if not os.path.exists(newName):
                    os.makedirs(newName)
                open(os.path.join(newName, 'index.txt'), 'w+').write(txt)
            elif len(districtCode) < 3:
                #print "%s: %s" % (stateCode, districtCode)
                txt = open(os.path.join(stateCode, districtCode, 'district.court', 'index.txt')).read()
                newName = '%s.%s' % (stateCode,districtCode)
                if not os.path.exists(newName):
                    os.makedirs(newName)
                open(os.path.join(newName, 'index.txt'), 'w+').write(txt)
        
if True:
    for stateCode in os.listdir('.'):
        if len(stateCode) == 2:
            for dirname, dirs, files in os.walk(stateCode, topdown=False):
                print dirname
                for filename in files:
                    print " +" + filename
                    os.unlink(os.path.join(dirname, filename))
                #for d in dirs:
                #    print " *" + d
                #    os.rmdir(os.path.join(dirname, d))
                os.rmdir(dirname)

#!/usr/bin/python
#-*- encoding: utf-8 -*-

import sys,os,re,shutil

top = "data/courts/jp"

for [dirname, dirs, files] in os.walk(top):
    for d in dirs:
        if d.endswith('.chiho.saibansho'):
            olddir = os.path.join(dirname, d)
            newdirStub = re.sub("\.chiho\.saibansho", "", d)
            newdir = os.path.join(dirname, newdirStub)
            if not os.path.exists(newdir):
                os.mkdir(newdir)
            olddir_fh = open(os.path.join(olddir, 'index.txt'))
            placeName = None
            placeEn = None
            while 1:
                line = olddir_fh.readline()
                if not line: break
                line = line.strip()
                line = line.decode('utf-8')
                if line.startswith('.. court:: '):
                    m = re.match(u"^\.\. court::\s*(.*)(地方裁判所)$", line)
                    placeName = m.group(1)
                    courtName = m.group(2)
                if line.startswith(':en:'):
                    m = re.match(u"^:en:\s+(.*?)\s+(District Court)$", line)
                    placeEn = m.group(1)
                    courtEn = m.group(2)
            olddir_fh.close()
            if not placeName or not placeEn:
                print "Oops!"
            newdir_fh = open(os.path.join(newdir, 'index.txt'), 'w+')
            newdir_fh.write(u".. category:: %s\n" % placeName)
            newdir_fh.write(u"   :category-id: blah\n")
            newdir_fh.write(u"   :en: %s\n" % placeEn)
            newdir_fh.close()

            chihoDir = os.path.join(newdir, 'chiho.saibansho')
            if not os.path.exists(chihoDir):
                shutil.move(olddir, chihoDir)
            oldKateiDir = os.path.join(dirname, newdirStub + '.katei.saibansho')
            kateiDir = os.path.join(newdir, 'katei.saibansho')
            if not os.path.exists(kateiDir):
                shutil.move(oldKateiDir, kateiDir)
            

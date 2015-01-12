#!/usr/bin/python
#-*- encoding: utf-8 -*-

import sys,os,re,shutil

top = "data/courts/jp"

for [dirname, dirs, files] in os.walk(top):
    if dirname.endswith('/koto.saibansho'):
        courtPath = os.path.join(dirname, 'index.txt')
        txt = open(courtPath).read()
        txt = re.sub("(?m).. court:: .*高等裁判所$", ".. court:: 高等裁判所", txt)
        txt = re.sub("(?m)   :en: .*High Court$", "   :en: High Court", txt)
        open(courtPath, "w+").write(txt)

#!/usr/bin/python
#-*- encoding: utf-8 -*-

import sys,os,re,shutil

top = "data/courts/jp"

for [dirname, dirs, files] in os.walk(top):
    if dirname.endswith('/chiho.saibansho'):
        courtPath = os.path.join(dirname, 'index.txt')
        txt = open(courtPath).read()
        txt = re.sub("(?m).. court:: .*地方裁判所$", ".. court:: 地方裁判所", txt)
        txt = re.sub("(?m)   :en: .*District Court$", "   :en: District Court", txt)
        open(courtPath, "w+").write(txt)
    if dirname.endswith('/katei.saibansho'):
        courtPath = os.path.join(dirname, 'index.txt')
        txt = open(courtPath).read()
        txt = re.sub("(?m).. court:: .*家庭裁判所$", ".. court:: 家庭裁判所", txt)
        txt = re.sub("(?m)   :en: .*Family Court$", "   :en: Family Court", txt)
        open(courtPath, "w+").write(txt)

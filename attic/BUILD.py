#!/usr/bin/python
#-*-encoding: utf-8 -*-

import re,sys,os,os.path

ifh = open("DATA.txt")

template = '''
.. court:: %s高等裁判所
   :court-id: jp;hc;%s.high.court
   :url: http://www.courts.go.jp

   .. reporter-key:: 刑集

   .. reporter-key:: 民集
'''

while 1:
    line = ifh.readline()
    if not line: break
    line = line.strip()
    DIR = line.split()[0]
    NAME = line.split()[1]
    NAME = re.sub("(県|都|府)$","",NAME)
    
    os.chdir(DIR)
    open("index.txt","w+").write(template % (NAME,DIR))
    os.chdir("..")

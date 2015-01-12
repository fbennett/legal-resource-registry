#!/usr/bin/python
#-*- encoding: utf-8 -*-

import sys,re,os

for dirname in os.listdir("."):
    if not os.path.isdir(dirname): continue
    ifh = open(os.path.join(dirname,"index.txt"))
    lines = []
    while True:
        line = ifh.readline()
        if not line: break
        line = line.rstrip()
        if not line: continue
        line = re.sub("地方", "家庭", line)
        line = re.sub("chiho", "katei", line)
        if re.match(".*reporter-key.*",line):
            continue
        lines.append(line)
    lines.append("")
    lines.append("   .. reporter-key:: 家月")
    txt = "\n".join(lines)
    newdir = re.sub("chiho","katei",dirname)
    os.makedirs(newdir)
    open(os.path.join(newdir,"index.txt"),"w+").write(txt)
    print newdir


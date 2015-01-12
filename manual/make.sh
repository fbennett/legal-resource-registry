#!/bin/bash

./egmaker.py --template=default.tex instructions.rst instructions.ltx
pdflatex instructions.ltx
pdflatex instructions.ltx
evince instructions.pdf

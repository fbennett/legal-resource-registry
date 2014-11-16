#!/bin/bash

./tools/grind-html-pages.py --stylesheet=legalcitem.css --link-stylesheet FederalCourts.rst
git commit -m "Updating site"
git subtree push --prefix=public git@github.com:jqheywood/CourtsSC.git gh-pages

#!/bin/bash

./tools/grind-html-pages.py --stylesheet=legalcitem.css --link-stylesheet FederalCourts.rst > public/index.html
./tools/grind-html-pages.py --stylesheet=legalcitem.css --link-stylesheet StateCourts.rst > public/states.html
git commit -m "Updating site" public
git subtree push --prefix=public git@github.com:jqheywood/CourtsSC.git gh-pages

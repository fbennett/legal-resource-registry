#!/bin/bash

cp doc-src/screen.css public
cp -r doc-src/bower_components public/
cp -r doc-src/graphics public/
cp -r doc-src/proofs-by-excel public/

#git add public
git commit -m "Updating site" public
#git subtree add --prefix public git@github.com:fbennett/legal-resource-registry.git gh-pages --squash
git subtree push --prefix=public git@github.com:fbennett/legal-resource-registry.git gh-pages

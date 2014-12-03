#!/bin/bash

./tools/pages.py
git commit -m "Updating site" public
git subtree push --prefix=public git@github.com:fbennett/legal-resource-registry.git gh-pages
git commit -m "Updating site" reporters-db
git subtree push --prefix=reporters-db git@github.com:fbennett/legal-resource-registry.git reporters-db

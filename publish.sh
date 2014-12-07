#!/bin/bash

git commit -m "Updating site" public
git subtree push --prefix=public git@github.com:fbennett/legal-resource-registry.git gh-pages

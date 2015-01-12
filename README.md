Legal Resource Registry
=======================

**License:** This repository is available under the permissive BSD license,
making it easy and safe to incorporate in your own libraries.

-----------------------------------------

Overview
--------

The Legal Resource Registry (LRR) a machine-readable description of courts and reporters
in individual national jurisdictions. The LRR contains files with non-ASCII filenames.
To work with the site in `git`, the following setting is required:

    git config core.quotepath false

Rendering
---------

To process the data, enter the root directory of the repo and run the following script:

    ./tools/pages.py
    
Use the `--help` option for guidance on options to the script:

    ./tools/pages.py --help

See the file `./tools/flp.py` for a sample export plugin.

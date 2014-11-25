Legal Resource Registry
=======================

Description
-----------

A registry for describing law-making entities, reporting services, and relations between them.

License
-------

This repository is available under the permissive BSD license, making it easy and safe to incorporate in your own libraries.

Pull and feature requests welcome. Online editing in GitHub is possible (and easy!)


-----------------------------------------

This is meant to be a canonical archive from which reporters.json can
be generated. The initial build was done with ad hoc scripts that are
described below (it should NOT be necessary to repeat this process).
At the end of the day, we will validate the output by comparing it
with the production copy of reporters.json that resides here:

    https://github.com/freelawproject/reporters-db
    
After round-trip validation is confirmed, future updates to
reporters.json can be derived from this archive.

^^^^^^^^^^^^^^
Original Build
^^^^^^^^^^^^^^

The starting point was `resource/resource.js`, taken from here:

   https://bitbucket.org/fbennett/free-law-ferret/src/143292e075493fa14e7eb61c6c1913d6915e1b3b/resource/constants/reporters.json

The original data in `resource/reporters.js` and `resource/courts.json`
was collected, collated and organized by the Free Law Project:

   https://github.com/mlissner/courtlistener/blob/master/alert/citations/constants.py

`mlz_jurisdiction` keys are added to the `resource/courts.json` object by the
`resource/COURTS.py` script, and written to `resource/courts-new.json`

The `resource/state_jur_map.json` object is derived from `resource/courts-new.json` by the
`resource/COURTS2.py` script.

`resource/reporters.js` has been hand-edited to add specific `mlz_jurisdiction`
values for specific courts.

The `tools/build-data.py` script resolves incomplete and remapped
`mlz_jurisdiction` values to align with those in `resource/courts-new.json`.

The `tools/pages.py` script builds the site.

^^^^^^^^^^
Production
^^^^^^^^^^

Only the `tools/pages.py` script will be used in production; the others
are one-off tools that will be moved to the attic.

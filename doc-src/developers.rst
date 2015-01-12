~~~~~~~
Liaison
~~~~~~~

Before making use of LRR court identifiers in a specific project,
please feel free to contact me (Frank Bennett
``<bennett@nagoya-u.jp>``) with a note of the role that LRR data will
play in your implementation.  This is a suggestion, not a demand, and
has *nothing whatsoever* to do with intellectual property claims et
cetera et cetera. It is just a matter of coordination: knowledge of
actual projects and use cases is our best guide to improving the
content of the repository.

~~~~~~~~~~~~~~~~
Cloning the Repo
~~~~~~~~~~~~~~~~

The LRR and the software for manipulating the content are contained in
a single GitHub repository. The command-line statement for a local read-only
clone of the project repo is::

    git clone https://github.com/fbennett/legal-resource-registry.git

Proposed changes can be submitted in the usual way, by forking the
repository and issuing pull requests from a revision branch.  The
statement for cloning a personal fork (where ``<my-id>`` is
replaced with your own GitHub ID, omitting the angle braces) is::

    git clone git@github.com:<my-id>/legal-resource-registry.git

~~~~~~~~~~~~~~~~~~~~~~
Page Processing Script
~~~~~~~~~~~~~~~~~~~~~~

Court and reporter details are stored under the ``./data`` subdirectory of
the repository root. The data can be ground into HTML pages using the
script at ``./tools/pages.py``. The ``--help`` option to the script
offers the following::

    Usage: 
    pages.py [option]
    
    Render website and export from Legal Resource Registry.
    
    Options:
      -h, --help            show this help message and exit
      -P PLUGIN, --plugin=PLUGIN
                            Process data using PLUGIN module.
      -w, --write-pages     Write page ouput (default is False).
      -s, --write-spreadsheets
                            Write spreadsheet ouput (default is False).
      -j JURISDICTION, --jurisdiction=JURISDICTION
                            Limit processing to specified jurisdiction.
    
    Happy hacking!

~~~~~~~~~~
Plugin API
~~~~~~~~~~

Details can be extracted from the files under ``./data`` in an
arbitrary form by casting a plugin for use with the ``pages.py``
script. Plugins are made up of three component parts:

1. A plugin-defined ``Data`` object holds data during processing;
2. Functions on a ``Hook`` class are used to manipulate data extracted from the repo; and
3. An ``Opt`` object accessible on ``Hook`` has several segments that provide some control over the records to be processed.

These components are described below. For worked examples of
plugin code, please refer to the file in the ``./tools/plugins``
subdirectory of the repository.

---------------------------

||||||||||||||||||
The ``Data`` class
||||||||||||||||||

This is just a bare class for carrying data segments during
processing: it can be defined any way you like. Since it is
installed as an argument to the main class object ``Hook``, it
can also be *called* anything you like. See the code block
in the next section for an example.

---------------------------

||||||||||||||||||
The ``Hook`` class
||||||||||||||||||

Five standard functions on the ``Hook`` class invoked during
page processing can be used to manipulate data extracted from
the repository. 

All functions have access to the ``Data`` object as ``self.data``.
During extraction, each court is read, followed by each of its
reporters. On completion, the ``self.export`` function is run to dump
the extracted data.

---------------------------

''''''''''''''''''''''''
self.court(options, arg)
''''''''''''''''''''''''

*arg* ``<string>``
    The name of the court, in the official script and language
    of the jurisdiction.

*options* ``<object>``
    The options set on the reStructuredText ``court`` directive,
    expressed as a set of key/value pairs. Test for the presence
    of options with ``options.has_key()``. Possible keys are:

    ``court-id``
        Always present. The ID of the court in URN syntax.

    ``url``
        Optional. The URL of a Web page with information on the court.

    ``en``
        Optional. The English translation of the court name. Present
        only when the court name is in a non-English language.

    ``flp-key``
        Optional. The Free Law Project identifier for the court.
        Relevant only to U.S. courts.
        'en': directives.unchanged

---------------------------

''''''''''''''''''''''''''''''''''''''''
self.reporter_start(options, dates, arg)
''''''''''''''''''''''''''''''''''''''''

*arg* ``<string>``
    The full name of the reporter, in the original script and
    language in which it is published.

*dates* ``<object>``
    The range of dates covered by the reporter, expressed as a set of
    key/value pairs. The elements (all of which are always present)
    are:


    ``startYearDisplay``
        The year from which the reporter begins, expressed as a
        four-digit integer.

    ``startYear``
        The year from which the reporter begins, expressed as a
        four-digit integer.
        
    ``startMonth``
        The month in which  the reporter begins, expressed as a
        two-digit integer with ``01`` origin.
        
    ``startDay``
        The day on which the reporter begins, expressed as a
        two-digit integer with ``01`` origin.
        
    ``endYearDisplay``
        Either "present" (for reporters currently active) or
        the year in which the reporter ends, expressed as a
        four-digit integer.

    ``endYear``
        Either boolean ``False`` or the year in which the reporter
        ends, expressed as a four-digit integer.
        
    ``endMonth``
        Either boolean ``False``, or the month in which the reporter
        ends, expressed as a two-digit integer with ``01`` origin.
        
    ``endDay``
        Either boolean ``False``, or the day on which the reporter
        ends, expressed as a two-digit integer with ``01`` origin.
        
*options* ``<object>``
    The options set on the reStructuredText ``reporter`` directive,
    expressed as a set of key/value pairs. Test for the presence
    of options with ``options.has_key()``. Possible keys are:

    ``jurisdiction``
        Always present. The lowest jurisdiction level containing
        all courts carried by the reporter edition, expressed in URN syntax.

    ``edition-abbreviation``
        Always present. The abbeviated form by which the reporter
        edition (such as "F.2d") is identified.

    ``dates``
        Always present. The raw record of the reporter edition
        date range, in the form "yyyy/mm/dd-yyyy/mm/dd".

    ``neutral``
        Optional. This key exists only on vendor-neutral citation
        forms.

    ``confirmed``
        Optional. When this key exists, the details of the
        reporter have been confirmed for accuracy.

    ``flp-series-cite-type``
        Optional. One of the following values (relevant only for U.S. reporters):

        * ``federal``
        * ``neutral``
        * ``scotus_early``
        * ``specialty``
        * ``specialty_lexis``
        * ``specialty_west``
        * ``state``
        * ``state_regional``

    ``flp-common-abbreviation``
        Optional. The abbreviated form of the full reporter
        name.



---------------------------

'''''''''''''''''''''''''''''''
self.reporter_end(options, arg)
'''''''''''''''''''''''''''''''

*options* ``<object>``
    Same as in ``self.reporter_start`` above.

*arg* ``<string>``
    Same as in ``self.reporter_start`` above.

---------------------------

'''''''''''''''''''
self.variation(arg)
'''''''''''''''''''

*arg* ``<string>``
    A variant abbreviation of the reporter edition currently being processed.

---------------------------

'''''''''''''
self.export()
'''''''''''''

The ``export()`` method has access to content stashed on ``self.data`` during processing.

---------------------------

|||||||||||||||||
The ``Opt`` class
|||||||||||||||||


*jurisdiction* ``<string>``
    A jurisdiction constraint, expressed in URN syntax. A
    jurisdiction given to the ``pages.py`` script with the
    ``-j`` option will override this value.

*conditional* ``<object>``
    This is a configuration option of limited utility, which collects
    a selected set of entries on a single page. It is used in the
    ``us_neutral.py`` plugin to generate the U.S. Neutral Citations
    page, and is unlikely to be useful for much else.

    Three keys must be set on the object:

    ``title``
        The title of the page.

    ``pageKey``
        The HTML page name.

    ``condition``
        An object with keys to be checked for presence
        on each reporters object. Court details will be
        output to the page only where at least one reporter is
        found to have this key.

---------------------------

Putting it all together, the following plugin code is (useless but) valid,
and will load and run without error::


    from LRR import Hook as HookBase

    class MyAmazingDataClass:
        def __init__(self):
            self.my_truth = False
            self.courts_in_english = []
    
    class Hook(HookBase):
        def __init__(self):
            HookBase.__init__(self, Data=MyAmazingDataClass)
            self.opt.jurisdiction = "jp"

        def court(self, options, arg):
            if options.has_key('en'):
                self.data.courts_in_english.append(options['en'])
            else:
                self.data.courts_in_english.append(arg)

        def reporter_start(self, options, dates, arg):
            pass

        def reporter_end(self, options, arg):
            pass

        def variation(self, arg):
            pass

        def export(self):
            self.data.courts_in_english.sort()
            for court in self.data.courts_in_english:
                print court

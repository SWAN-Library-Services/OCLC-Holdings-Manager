# OCLC-Holdings-Manager

OCLC Holdings Manager is a rule-based utility that analyzes MARC21 extracts and
determines changes between datasets.  This comparison is then used to set and
unset WorldCat holdings using the OCLC WorldCat Metadata API.  OHM was designed
to be consortia ready, but should work just fine for standalone libraries as
well.

This tool relies on a properly configured OCLC WSKey to work.  You will need an
OCLC symbol that has permissions to make changes on behalf of all configured 
symbols.  OCLC support should be able to assist in proper configuration.

To begin, you will need to modify the example settings file to fit the format
of your MARC21 extracts.  Exclusions are configurable on entire Bib records,
individual items, or both.  A mapping from ILS library identifiers to OCLC 
symbols is used to determine holdings.  Multiple ILS libraries can share a
single OCLC symbol without issue, but one library cannot have multiple OCLC
symbols.

The menu.py will make use of the parameters from the settings.json or 
settings-<name>.json file.  You then have the option to import holdings data
from a MARC21 extract, compare datasets, and in the next version send changes 
to OCLC.  There is also a test to verify that an OCLC WSKey has all appropriate
permissions to set holdings for all institutions.

OHM requires Python 3.6 or higher to run, but sees vast speed improvements
using PyPy3.6 or above.  Please note that a 64-bit version of either is requred
if your MARC21 files are larger than 4GB in size.
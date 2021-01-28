# pyamidict

Tools to manage dictionaries - Create, Update, Validate

`editor` does editing; `schematron` does the validation

## overview
### amidict
A `Dictionary` class to read an xml file, be cleaned with an XSLT, and save result.

### schematron
The ZVON tutorial
http://www.zvon.org/xxl/SchematronTutorial/General/toc.html


## running
### amidict
````
cd <pythoncode_dir>
python pyamidict/amidict_runner.py 
````


## inventory
(comments as #foo)

````
.
├── README.md
├── __init__.py
├── amidict_runner.py   # runs the Python as a script. Mainly for testing
├── editor              # package for editing and validating
│   ├── __init__.py
│   ├── amidict.py.     # Dictionary class
│   └── schematron.py.  # schematron validator
├── main.py             # testing?
├── notes.txt
├── resources                       # files used by editor		§	§	§	 
│   ├── clean_dict.xsl              # XSLT to clean old dictionaries into conformant versions
│   ├── country6.update.xml        
│   ├── country6.xml                # truncated country dictionary      
│   ├── dict_requirements.md        # requirements - please add
│   ├── openVirus.schematron.xml.   # schematron tests
│   ├── openVirus_schema.xsd.       # schema
│   ├── simple.xml                  # minimal dictionary
│   ├── simple_wiki_bad.xml         # deliberate errors for testing
├── temp                 # converted (cleaned) dictionaries from `dictionary` 2020-11 repository
│   ├── country.xml
│   ├── country6.xml
│   ├── disease.xml
│   ├── drug.xml
│   ├── npi.xml
│   ├── organization.xml
│   ├── simple_wiki_bad.xml
│   ├── test_trace.xml
│   ├── virus.xml
│   └── zoonosis.xml
├── test_runner.py              # runs tests
└── tests                       # test suites
    ├── __init__.py
    ├── schematron_test.py
    └── test_editor.py
````
# pyamidict.editor.amidict.py
"""
Dictionary class delegates XML to included object
No subclassing
"""
import xml.etree.ElementTree as ET
import copy
import os
import re
import sys

# elements
DICTIONARY = "dictionary"
DESCRIPTION = "description"
ENTRY = "entry"
METADATA = "metadata"
SYNONYM = "synonym"

# attributes
ID = "id"
DESCRIPTION_A = "description"
NAME = "name"
TERM = "term"
TITLE = "title"
WIKIDATA_ID = "wikidataID"
WIKIDATA_URL = "wikidataURL"
WIKIPEDIA_EN_PAGE = "wikipediaPage"
WIKIPEDIA_EN_URL = "wikipediaURL"

ALLOWED_WIKIDATA_REGEX = "_"
XML_LANG = "xml:lang"

SUPPORTED_ATTS = [
    DESCRIPTION_A,
    ID,
    NAME,
    TERM,
    TITLE,
    WIKIDATA_ID,
    WIKIDATA_URL,
    WIKIPEDIA_EN_PAGE,
    WIKIPEDIA_EN_URL,
]

REGEXES = {
    WIKIDATA_ID : "(Q|P)\d+",
    WIKIDATA_URL : "https?://www\.wikidata\.org/entity/(Q|P)\d+",
    WIKIPEDIA_EN_PAGE: "(https?://en\.wikipedia\.org/wiki/)?[A-Z0-9][^\s]+", # we are undecided on this attribute
    WIKIPEDIA_EN_URL: "https?://en\.wikipedia\.org/wiki/[A-Z0-9][^\s]+",
}

WIKIDATA_ATTRIBUTE_REGEX = "_([PpQq])\d+_([a-z][a-z0-9]+)"

class Dictionary():

    """
    constructor
    creates Dictionary as wrapper to XML
    :elem: dictionary in XML. Maybe
    """

    def __init__(self, elem=None, file=None):
        self.err_count = 0;
        self.max_err = 2;
        self.unknown_atts = set()
        if not file is None:
            if not os.path.exists(file):
                raise Exception ("file not found: "+file)
            self.xml_dict = self.read_dictionary_element(file)
        elif not elem is None:
            self.xml_dict = elem
        else:
            print("empty dictionary")

    def read_dictionary_element(self, file):
        self.file = file
        with open(file, "r") as f:
            dictionary_text = f.read();
        root = ET.fromstring(dictionary_text)
        if root.tag != DICTIONARY:
            raise Exception ("not a dictionary file")
        if not os.path.split(file)[-1] == root.attrib[TITLE]+".xml":
            print("Dictionary @title should equal filename")


        return root

    def get_descendant_elements(self, tag):
        if not self.xml_dict is None:
            descendants = self.xml_dict.findall(tag)
        return descendants

    def get_synonyms(self, entry):
        return list(entry.findall(SYNONYM)) if entry.tag == ENTRY else None

    def get_descriptions(self, entry):
        return list(entry.findall(DESCRIPTION)) if entry.tag == ENTRY else None

    def get_wikidata_id(self, entry):
        return entry.attrib[WIKIDATA_ID]

    def get_supported_attribute(self, entry, att_name):
        value = None
        if att_name in SUPPORTED_ATTS:
            value = entry.attrib[att_name]
            if not self.check_reserved_att_name_value(value, att_name):
#                print("unreserved attribute", att_name)
                value = None
        return value

    def check_entry_attributes(self, entry):
        for att_name in entry.attrib:
            if self.get_supported_attribute(entry, att_name):
                pass
            elif self.check_wikidata_attribute(att_name):
                pass
            elif att_name not in SUPPORTED_ATTS:
#                print("unknown attribute", att_name)
                self.unknown_atts.add(att_name)

    def check_entry_children(self, entry):
#        print("WARNING check_entry_children NYI")
        pass

    def analyze_entry(self, entry):
        self.check_entry_attributes(entry)
        self.check_entry_children(entry)

        # https://realpython.com/iterate-through-dictionary-python/??
#        print(self.get_supported_attribute(entry, WIKIDATA_ID))
#        print(self.get_supported_attribute(entry, WIKIDATA_URL))
#        print(self.get_supported_attribute(entry, WIKIPEDIA_EN_PAGE))
#        print(self.get_supported_attribute(entry, WIKIPEDIA_EN_URL))
#        print("synonyms",  list(map(entry_text, self.get_synonyms(entry))))
#        print("descriptions",  list(map(entry_text, self.get_descriptions(entry))))

    def get_entries(self):
        return self.get_descendant_elements(ENTRY)

    def check_wikidata_attribute(self, att_name) :
#        print("testing wikidata name", att_name)
        regex = re.compile(WIKIDATA_ATTRIBUTE_REGEX)
        return regex.match(att_name)

    def check_reserved_att_name_value(self, value, att_name):
        if att_name in REGEXES:
            regex = re.compile(REGEXES[att_name])
            if not regex.match(value):
                if self.err_count < self.max_err:
                    self.err_count += 1
                    print(att_name + ":", value, "does not match ", regex)
                return False
        return True

    def analyze(self):
        entries = self.get_descendant_elements(ENTRY)
        print("entries", len(entries))
        for entry in entries:
            self.analyze_entry(entry)


def entry_text(entry):
    return entry.text

def entry_lang(entry):
    lang = entry.attrib["xml:lang"]
    lang = "en" if lang is None else lang

def get_resources():
    PYAMIDICT = os.path.normpath(os.path.join(__file__, "..", ".."))
    RESOURCE_DIR = os.path.join(PYAMIDICT, "resources")
    DICTIONARY_DIR = os.path.normpath(os.path.join(PYAMIDICT, "..", "..", "openVirus202011"))
    print("DD", DICTIONARY_DIR)
    return (PYAMIDICT, RESOURCE_DIR, DICTIONARY_DIR)


def main():
    PYAMIDICT, RESOURCE_DIR, DICT202011 = get_resources()
    COUNTRY_DICT = os.path.join(DICT202011, "country", "country.xml")
    dict_files = {
        os.path.join(RESOURCE_DIR, "country6.xml"),
        COUNTRY_DICT,
        os.path.join(DICT202011, "disease", "disease.xml"),
        os.path.join(DICT202011, "drug", "drug.xml"),
        os.path.join(DICT202011, "npi", "npi.xml"),
        os.path.join(DICT202011, "organization", "organization.xml"),
        os.path.join(DICT202011, "test_trace", "test_trace.xml"),
        os.path.join(DICT202011, "virus", "virus.xml"),
        os.path.join(DICT202011, "zoonosis", "zoonosis.xml")
    }
    for dict_file in dict_files:
        dictionary = Dictionary(file=dict_file)
        print("running dictionary", dict_file)
        dictionary.analyze()
        if len(dictionary.unknown_atts) > 0:
            print("unknown attributes", dictionary.unknown_atts)


if __name__ == "__main__":
    main()

## TODO
# rename old attribute names
# move attributes to child elements
# delete entries
# add entries from file
# add metadata records


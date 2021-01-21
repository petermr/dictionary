# pyamidict.editor.amidict.py
"""
Dictionary class delegates XML to included object
No subclassing
"""
import xml.etree.ElementTree as ET
#from typing import hints
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

ALT_NAMES = "altNames"

ALLOWED_WIKIDATA_REGEX = "_"
XML_LANG = "xml:lang"
LANG_EN = "en"
LANGUAGES = {
    "Chinese"    : "ZH",
    "English"    : "EN",
    "French"     : "FR",
    "German"     : "DE",
    "Hindi"      : "HI",
    "Kannada"    : "KN",
    "Malayalam"  : "ML",
    "Portuguese" : "PT",
    "Sanskrit"   : "SA",
    "Spanish"    : "ES",
    "Tamil"      : "TA",
    "Urdu"       : "UR",
}


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

UNWANTED_ATTS = [
    ALT_NAMES,
]

SUPPORTED_CHILDREN = [
    DESCRIPTION,
    SYNONYM
]

REGEXES = {
    WIKIDATA_ID : "(Q|P)\d+",
    WIKIDATA_URL : "https?://www\.wikidata\.org/(wiki|entity)/(Q|P)\d+",
    WIKIPEDIA_EN_PAGE: "(https?://en\.wikipedia\.org/wiki/)?(%[A-F0-9][A-F0-9]|[A-Z0-9])[^\s]+", # we are undecided on this attribute
    WIKIPEDIA_EN_URL: "https?://en\.wikipedia\.org/wiki/(%[A-F0-9][A-F0-9]|[A-Z0-9])[^\s]+",
}

WIKIDATA_ATTRIBUTE_REGEX = re.compile("_([PpQq])\d+_([a-z][a-z0-9]+)")

OPEN_VIRUS_DICT_NAMES = ["country", "disease", "drug", "npi",
                          "organization", "test_trace", "virus", "zoonosis"]

def get_resources():
    PYAMIDICT = os.path.normpath(os.path.join(__file__, "..", ".."))
    RESOURCE_DIR = os.path.join(PYAMIDICT, "resources")
    TEMP_DIR = os.path.join(PYAMIDICT, "temp")
    DICTIONARY_VERSION = "openVirus202011"
    DICTIONARY_VERSION = "openVirus20210120"
    DICTIONARY_TOP = os.path.normpath(os.path.join(PYAMIDICT, "..", ".."))
    DICTIONARY_DIR = os.path.join(DICTIONARY_TOP, DICTIONARY_VERSION)
    return (PYAMIDICT, RESOURCE_DIR, DICTIONARY_DIR, TEMP_DIR)


PYAMIDICT, RESOURCE_DIR, DICT202011, TEMP_DIR = get_resources()

class Entry():

    def __init__(self, elem=None, dict=None):
        self.elem = elem
        self.dict = dict
        self.deleted_atts = []

    def tidy_entry(self):
        self.transfer_description_atts_to_child()
        self.remove_deleted_atts(UNWANTED_ATTS)
        if self.change:
#            print(ET.tostring(self.elem))
            pass

    def add_lang_child(self, tag, lang, attname, deleted_atts):
        child = ET.Element(tag)
        child.set(XML_LANG, lang)
        child.text = self.elem.get(attname)
        self.elem.append(child)
        deleted_atts.append(attname)

    def transfer_description_atts_to_child(self):
        change = False
        deleted_atts = []
        for attname in self.elem.attrib:
            if "_description" in attname:
                lang = attname.split("_")[0]
                if lang in LANGUAGES:
                    self.add_lang_child(DESCRIPTION, lang, attname, deleted_atts)
                else:
                    print("UNKNOWN lang:", lang)
            elif attname in LANGUAGES:
                value = self.elem.attrib[attname]
                if WIKIDATA_ATTRIBUTE_REGEX.match(value):
                    print("rejected untranslated name")
                else:
                    lang = attname
                    self.add_lang_child(SYNONYM, lang, attname, deleted_atts)
        self.remove_deleted_atts(UNWANTED_ATTS)

    def remove_deleted_atts(self, deleted_atts):
        self.change = False
        if deleted_atts:
            self.change = True
            for attname in deleted_atts:
                if attname in self.elem.attrib:
                    del self.elem.attrib[attname]

    def entry_text(self):
        return self.elem.text

    def entry_lang(self):
        lang = self.elem.attrib[XML_LANG]
        lang = LANG_EN if lang is None else lang


    def analyze(self):
        self.check_entry_attributes()
        self.check_entry_children()

    def get_name(self):
        return self.elem.attrib[NAME]

    def get_attribute_names(self):
        return {k for k in self.elem.attrib}

    def get_synonyms(self):
        return list(self.elem.findall(SYNONYM)) if self.elem.tag == ENTRY else None

    def get_descriptions(self):
        return list(self.elem.findall(DESCRIPTION)) if self.elem.tag == ENTRY else None

    def get_wikidata_id(self):
        return self.elem.attrib[WIKIDATA_ID] if WIKIDATA_ID in self.elem.attrib else None

    def get_supported_attribute(self, att_name):
        value = None
        if att_name in SUPPORTED_ATTS:
            value = self.elem.attrib[att_name]
            if not self.check_reserved_att_name_value(value, att_name):
                value = None
        return value

    def check_entry_attributes(self):
        for att_name in self.elem.attrib:
            if self.get_supported_attribute(att_name):
                pass
            elif self.check_wikidata_attribute(att_name):
                pass
            elif att_name not in SUPPORTED_ATTS:
                self.dict.unknown_atts.add(att_name)

    def check_entry_children(self):
        children = list(self.elem)
        for child in children:
            if child.tag in SUPPORTED_CHILDREN:
                pass
            else:
                print("unsupported child of entry", child.tag)

    def check_wikidata_attribute(self, att_name) :
        self.check_wikidata_exists(att_name)
        return WIKIDATA_ATTRIBUTE_REGEX.match(att_name)

    def check_wikidata_exists(self, att_name):
        # TODO create Wikidata lookup
        pass

    def check_reserved_att_name_value(self, value, att_name):
        if att_name in REGEXES:
            regex = re.compile(REGEXES[att_name])
            if not regex.match(value):
                if self.err_count < self.max_err:
                    self.err_count += 1
                    print(att_name + ":", value, "does not match ", regex)
                return False
        return True

    @classmethod
    def merge_entries(cls, entrylist):
        el = [entrylist[0]]
        entry_set = set()
        for i in range(0, len(entrylist)):
            entry_set.add(entrylist[i])
        print ("len set", len(set))

    def __hash__(self):
        return None

    def __eq__(self, other):
        if not isinstance(other, Entry):
            print("NE")
            return NotImplemented
        if set(self.get_attribute_names()) != set(other.get_attribute_names()):
            print ("unequal attribute names")
            return False
        return True




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
        self.entry_list_by_wikidata_id = {}

        if not file is None:
            if not os.path.exists(file):
                raise Exception ("file not found: "+file)
            self.file = file
            self.root = self.read_dictionary_element(file)
        elif not elem is None:
            self.root = elem
        else:
            print("empty dictionary")

    def read_dictionary_element(self, file) -> ET.Element:
        self.file = file
        with open(file, "r") as f:
            dictionary_text = f.read();
        self.root = ET.fromstring(dictionary_text)
        if self.root.tag != DICTIONARY:
            raise Exception ("not a dictionary file")
        if not os.path.split(file)[-1] == self.root.attrib[TITLE]+".xml":
            print(os.path.split(file)[-1], "//", self.root.attrib[TITLE]+".xml")
            print("Dictionary @title should equal filename")
        return self.root

    def get_descendant_elements(self, tag):
        if not self.root is None:
            return self.root.findall(tag)
        else:
            raise Exception("No XML Element in dictionary")

    def get_entries(self):
        return [Entry(elem=e, dict=self) for e in self.get_descendant_elements(ENTRY)]

    def analyze(self):
        entries = self.get_entries()
        print("entries", len(entries))
        for entry in entries:
            entry.analyze()

    def tidy_old_dictionary(self):
        """clean original dictionaries; this should become obsolete"""
        entries = self.get_entries()
        for entry in entries:
            entry.tidy_entry()
        self.create_entry_list_by_wikidata_id()
        self.write_outfile()

    def write_outfile(self):
        outfile = os.path.join(TEMP_DIR, os.path.split(self.file)[-1])
        with open(outfile, "wb") as f:
            f.write(ET.tostring(self.root))
        print("wrote", outfile,"\n")

    def xsl_transform(self, xsl_file, outdir=TEMP_DIR):
        """still struggling with XSLT, will hardcode transforms"""
        import lxml.etree as ET
        root1 = ET.parse(self.file)
        xsl = ET.parse(xsl_file)
        transform = ET.XSLT(xsl)
        newdom = transform(root1)
        outfile = os.path.join(TEMP_DIR, os.path.split(self.file)[-1])
        with open(outfile, "wb") as f:
            f.write(ET.tostring(newdom, pretty_print=True))
        print("wrote", outfile,"\n")

    def create_entry_list_by_wikidata_id(self):
        self.entry_list_by_wikidata_id = {}
        entries = self.get_entries();
        for entry in entries:
            id = entry.get_wikidata_id()
            if id is not None:
                if id not in self.entry_list_by_wikidata_id:
                    self.entry_list_by_wikidata_id[id] = [entry]
                else:
                    self.entry_list_by_wikidata_id.get(id).append(entry)
        return self.entry_list_by_wikidata_id

    def merge_duplicate_wikidata_ids(self):
        elid = self.create_entry_list_by_wikidata_id()
        multiple = [value[0].get_wikidata_id() for k, value in elid.items() if len(value) > 1]
        print("mult", multiple)
        for w_id in multiple:
            entrylist = [e for e in elid.get(w_id)]
            enew = Entry.merge_entries(entrylist)








def get_remote_dictionary_files(dict_dir, dictionary_names):
    return [os.path.join(os.path.join(dict_dir, name), name+".xml") for name in dictionary_names]

def main():

    dict_files = get_remote_dictionary_files(DICT202011, OPEN_VIRUS_DICT_NAMES)
    for dict_file in dict_files:
        dictionary = Dictionary(file=dict_file)
        print("running dictionary", dict_file)
        dictionary.analyze()
        dictionary.tidy_old_dictionary()
        if len(dictionary.unknown_atts) > 0:
            print("unknown attributes", dictionary.unknown_atts)
        dictionary.merge_duplicate_wikidata_ids()


#        xsl_file = os.path.join(RESOURCE_DIR, "clean_dict.xsl")
#        dictionary.xsl_transform(xsl_file)

    print("end of transform")

if __name__ == "__main__":
    main()
else:
    main()


## TODO
# delete entries
# add entries from file
# add metadata records


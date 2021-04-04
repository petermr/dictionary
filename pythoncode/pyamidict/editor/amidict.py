# pyamidict.editor.amidict.py
"""
Dictionary class delegates XML to included object
No subclassing
"""
import xml.etree.ElementTree as ET
#from typing import hints
import os
import re

# elements
DICTIONARY = "dictionary"
DESCRIPTION = "description"
ENTRY = "entry"
METADATA = "metadata"
RELATED = "relatedItem"
SYNONYM = "synonym"

# attributes
ID = "id"
IDX = "idx"
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
    "Chinese":     "ZH",
    "English":     "EN",
    "French":      "FR",
    "German":      "DE",
    "Hindi":       "HI",
    "Kannada":     "KN",
    "Malayalam":   "ML",
    "Portuguese":  "PT",
    "Sanskrit":    "SA",
    "Spanish":     "ES",
    "Tamil":       "TA",
    "Urdu":        "UR",
}


SUPPORTED_ATTS = [
    DESCRIPTION_A,
    ID,
    IDX,
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
    RELATED,
    SYNONYM
]

REGEXES = {
    WIKIDATA_ID: "(Q|P)\d+",
    WIKIDATA_URL: "https?://www\.wikidata\.org/(wiki|entity)/(Q|P)\d+",
    # we are undecided on this attribute
    WIKIPEDIA_EN_PAGE: "(https?://en\.wikipedia\.org/wiki/)?(%[A-F0-9][A-F0-9]|[A-Z0-9])[^\s]+",
    WIKIPEDIA_EN_URL: "https?://en\.wikipedia\.org/wiki/(%[A-F0-9][A-F0-9]|[A-Z0-9])[^\s]+",
}

WIKIDATA_ATTRIBUTE_REGEX = re.compile("_([PpQq])\d+_([a-z][a-z0-9]+)")

OPEN_VIRUS_DICT_NAMES = [
    "country",
    "disease",
    "drug",
    "npi",
    "organization",
    "test_trace",
    "virus",
    "zoonosis"
]

TRANSFORMED_ATTS = {
    "country": "_p297_country",
    "crossrefid": "_p3153_crossref_funder_id"
}

def get_resources_base():
    PYAMIDICT = os.path.normpath(os.path.join(__file__, "..", ".."))
    RESOURCE_DIR = os.path.join(PYAMIDICT, "resources")
    TEMP_DIR = os.path.join(PYAMIDICT, "temp")
    DICTIONARY_VERSION = "openVirus202011"
    DICTIONARY_VERSION = "openVirus20210120"
    DICTIONARY_TOP = os.path.normpath(os.path.join(PYAMIDICT, "..", ".."))
    DICTIONARY_DIR = os.path.join(DICTIONARY_TOP, DICTIONARY_VERSION)
    return (PYAMIDICT, RESOURCE_DIR, DICTIONARY_DIR, TEMP_DIR, DICTIONARY_TOP)


PYAMIDICT, RESOURCE_DIR, DICT202011, TEMP_DIR, DICTIONARY_TOP = get_resources_base()

class Resources():
    def __init__(self):
        pass

    def get_resources(self):
        return get_resources_base()

class Entry():

    def __init__(self, elem=None, dictionary=None):
        self.elem = elem
        self.dictionary = dictionary
        self.deleted_atts = []

    def tidy_entry(self):
        self.transfer_description_atts_to_child()
        self.remove_deleted_atts(UNWANTED_ATTS)
        if self.change:
            print("changed", ET.tostring(self.elem))
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
                self.transfer_att_language_desc_to_child(attname, deleted_atts)
            elif attname in LANGUAGES:
                self.transfer_lang_att_to_child_synonym(attname, deleted_atts)
        self.remove_deleted_atts(UNWANTED_ATTS)

    def transfer_lang_att_to_child_synonym(self, attname, deleted_atts):
        value = self.elem.attrib[attname]
        if WIKIDATA_ATTRIBUTE_REGEX.match(value):
            print("rejected untranslated name")
        else:
            lang = attname
            self.add_lang_child(SYNONYM, lang, attname, deleted_atts)

    def transfer_att_language_desc_to_child(self, attname, deleted_atts):
        lang = attname.split("_")[0]
        if lang in LANGUAGES:
            self.add_lang_child(DESCRIPTION, lang, attname, deleted_atts)
        else:
            print("UNKNOWN lang:", lang)

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

    def get_relatedItems(self):
        return list(self.elem.findall(RELATED)) if self.elem.tag == ENTRY else None

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
                self.dictionary.unknown_atts.add(att_name)

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
                if self.dictionary.err_count < self.dictionary.max_err:
                    self.dictionary.err_count += 1
                    print(att_name + ":", value, "does not match ", regex)
                return False
        return True

    @classmethod
    def merge_entries_common_wid(cls, entrylist):
        # how many unique wikidata_ids?
        entry_set = set()
        for i in range(0, len(entrylist)):
            entry_set.add(entrylist[i])
        entrylist = list(entry_set)

        if len(entry_set) > 1:
            deletable_list = []
            for i in range(1, len(entrylist)):
                if entrylist[0].get_wikidata_id() == entrylist[i].get_wikidata_id():
                    # record merge
                    entrylist[0].elem.attrib["merged"] = "true"
                    entrylist[0].merge_attributes(entrylist[i])
                    entrylist[0].merge_children(entrylist[i])
                    deletable_list.append(entrylist[i])
#                    print("deleting", entrylist[i])
#            print(ET.tostring(entrylist[0].elem))

    #            for xx in entry_set:
#                print(ET.tostring(xx.elem))

    def merge_attributes(self, other_entry):
        for attname in other_entry.elem.attrib:
            other_val = other_entry.elem.attrib[attname]
            if attname in self.elem.attrib:
                attvalue = self.elem.attrib[attname]
                if isinstance(attvalue, list):
                    # multiple fields, add new one
                    if other_val not in attvalue:
                        attvalue.append(other_val)

                elif attvalue != other_val:
                    # single old field, make list
                    attvalue = [attvalue, other_val]
                self.elem.attrib[attname] = attvalue

    def merge_children(self, other_entry):
        pass

    def __hash__(self):
        """this is awful but Element  doesn't have a hash"""
        # we assume that the string is canonical
        return hash(ET.canonicalize(xml_data=ET.tostring(self.elem)))

    def __eq__(self, other):
        if not isinstance(other, Entry):
#            print("NE")
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
        self.err_count = 0
        self.max_err = 2
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
        """read XML file and parse into XML element

        *file* XML file to read and parse

        raise ParseError if XML is not well-formed

        return Parsed XML as ElementTree element or None
        """

        self.file = file
        with open(file, "r") as f:
            dictionary_text = f.read()
        try:
            self.root = ET.fromstring(dictionary_text)
        except ET.ParseError as e:
            print("XML parse error", e)
            return None
        if self.root.tag != DICTIONARY:
            raise Exception ("not a dictionary file")
        title_ = self.root.attrib[TITLE]
        if not os.path.split(file)[-1] == title_ + ".xml":
#            print(os.path.split(file)[-1], "//", self.root.attrib[TITLE]+".xml")
            print("Dictionary @title", title_, "should equal filename", file)
        return self.root

    def get_descendant_elements(self, tag):
        if self.root is not None:
            return self.root.findall(tag)
        else:
            print("No XML root in dictionary")
            return []

    def get_entries(self):
#        print("get entries***********")
        entry_list = [Entry(elem=e, dictionary=self) for e in self.get_descendant_elements(ENTRY)]
        for i in range(len(entry_list)):
            entry_list[i].elem.attrib["idx"] = str(i)
#        print(ET.tostring(entry_list[i].elem))
        return entry_list

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
        print("writing to", outfile)
        with open(outfile, "wb") as f:
            try :
                f.write(ET.tostring(self.root))
            except:
                print("Cannot write tree to", outfile)

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
        print("wrote transform", outfile,"\n")

    def create_entry_list_by_wikidata_id(self):
        self.entry_list_by_wikidata_id = {}
        entries = self.get_entries()
        for entry in entries:
            id = entry.get_wikidata_id()
            if id is not None:
                if id not in self.entry_list_by_wikidata_id:
                    self.entry_list_by_wikidata_id[id] = [entry]
                else:
                    self.entry_list_by_wikidata_id.get(id).append(entry)
        return self.entry_list_by_wikidata_id

    def merge_duplicate_wikidata_ids(self):
        entry_list_by_wid = self.create_entry_list_by_wikidata_id()
        multiple = [entry_lst[0].get_wikidata_id() for k, entry_lst in entry_list_by_wid.items() if len(entry_lst) > 1]
        if len(multiple) > 1:
#            print("multiple", multiple)
            pass
        for w_id in multiple:
            entrylist = [e for e in entry_list_by_wid.get(w_id)]
            enew = Entry.merge_entries_common_wid(entrylist)
#        parent_map = {c: p for p in tree.iter() for c in p}
# https://towardsdatascience.com/processing-xml-in-python-elementtree-c8992941efd2
# root.findall("./genre/decade/movie/format[@multiple='Yes']..."):



# end class Entry
def get_remote_dictionary_files(dict_dir, dictionary_names):
    return [os.path.join(os.path.join(dict_dir, name), name+".xml") for name in dictionary_names]

def test_browse(dict_file):
    dictionary = Dictionary(file=dict_file)
    print("running dictionary", dict_file)
    dictionary.analyze()
    dictionary.tidy_old_dictionary()
    if len(dictionary.unknown_atts) > 0:
        print("unknown attributes", dictionary.unknown_atts)
    dictionary.merge_duplicate_wikidata_ids()
    dictionary.write_outfile()

def test1():
    TEST_DICT = os.path.join(DICTIONARY_TOP, "test")
    test_file = os.path.join(TEST_DICT, "eo_test1.xml")
    print("testing", test_file)
    test_browse(test_file)


def main():
    """
    dict_names = OPEN_VIRUS_DICT_NAMES
 #   dict_names = ["test_trace"]
    dict_files = get_remote_dictionary_files(DICT202011, dict_names)
    
    """

#    test_browse_current_dicts()
    test1()


def test_browse_current_dicts():
    CEVOPEN_DICT = os.path.join(DICTIONARY_TOP, "cevopen")
    dict_files = [
        os.path.join(CEVOPEN_DICT, "activity", "eo_activity.xml"),
        os.path.join(CEVOPEN_DICT, "analysis", "eo_analysis_method.xml"),
        os.path.join(CEVOPEN_DICT, "compound", "eo_compound.xml"),
        os.path.join(CEVOPEN_DICT, "extraction", "eo_extraction.xml"),
        os.path.join(CEVOPEN_DICT, "gene", "eo_plant_gene.xml"),
        os.path.join(CEVOPEN_DICT, "genus", "eo_plant_genus.xml"),
        os.path.join(CEVOPEN_DICT, "plant", "eo_plant.xml"),
        os.path.join(CEVOPEN_DICT, "plant_part", "eo_plant_part.xml"),
        os.path.join(CEVOPEN_DICT, "target", "eo_target_organism.xml")
    ]
    for dict_file in dict_files:
        test_browse(dict_file)


#    test_merge(os.path.join(RESOURCE_DIR, "test_multiple.xml"))


#        xsl_file = os.path.join(RESOURCE_DIR, "clean_dict.xsl")
#        dictionary.xsl_transform(xsl_file)


if __name__ == "__main__":
    main()
else:
    main()


## TODO
# delete entries
# add entries from file
# add metadata records

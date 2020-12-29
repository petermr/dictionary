import xml.etree.ElementTree as ET

class Dictionary():
    """A dictionary in representable in XML"""
    DICTIONARY  = "dictionary"
    DESCRIPTION = "description"
    ENTRY       = "entry"
    METADATA    = "metadata"
    SYNONYM     = "synonym"

    DESCRIPTION_A     = "description"
    NAME_A            = "name"
    TITLE_A     = "title"
    TITLE_A     = "title"
    XML_LANG_A  = "xml:lang"


    def __init__(self):
        pass

    def Dictionary(self):
        pass

    @staticmethod
    def read_dictionary_as_text(dictionary_file):
        with open(dictionary_file, "r") as f:
            dictionary = f.read();
        return dictionary

    @staticmethod
    def read_dictionary_element(dictionary_file):
        dictionary_text = Dictionary.read_dictionary_as_text(dictionary_file)
        root = ET.fromstring(dictionary_text)
        rootx = ET.ElementTree()
#        print("class", root.__class__, rootx.__class__)
        return root

    @staticmethod
    def read_dictionary(dictionary_file):
        dictionary = Dictionary()
        dictionary.element = Dictionary.read_dictionary_element(dictionary_file)
        return dictionary


    @staticmethod
    def DICTIONARY_TAG():
        return "dictionary"


class Description():
    pass

class Entry():
    pass

class Metadata():
    pass

class Synonym():
    pass

print("dict.py")
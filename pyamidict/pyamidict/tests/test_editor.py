# reading tests

from pyamidict.editor.dict import Dictionary
import os
import unittest
import xml.etree.ElementTree as ET
import xmlschema

class TestEditor(unittest.TestCase):

    RESOURCES = "resources"
    RESOURCE_DIR = os.path.join("..", RESOURCES)
    simple_xml_file = os.path.join(RESOURCE_DIR, "simple.xml")


    def setUp(self):
        self.root_element = Dictionary.read_dictionary_element(self.simple_xml_file)
        self.simple_dictionary = Dictionary.read_dictionary(self.simple_xml_file)

    def test_read_dictionary(self):
#        print("dir for ed", dir(read))
        text = Dictionary.read_dictionary_as_text(self.SIMPLE_XML_FILE)
        self.assertIsNotNone(text)
#        print(text)
        expected = """<dictionary title="simple" xmlns:xml="http://www.w3.org/XML/1998/namespace">
  <metadata date="2020-08-09" source="AMI kangaroo">simple</metadata>
  <entry id="oldID" name="simple1" term="simple1" description="simple1" wikidataID="foo" wikidataURL="https://"
         wikipediaPage="foo" wikipediaURL="https://" source="SPARQL query">
    <synonym xml:lang="en">very simple</synonym>
  </entry>
</dictionary>
"""
# this might vary
        self.assertEqual(expected, text)

    def test_read_dictionary_XML(self):
        root = Dictionary.read_dictionary_element(self.SIMPLE_XML_FILE)
        self.assertIsNotNone(root)

    def test_create_dictionary(self):
        self.DICTIONARY = Dictionary.read_dictionary(self.SIMPLE_XML_FILE)

    def test_validate_dictionary(self):
        import xmlschema
        xmlschema.validate('doc.xml', 'some.xsd')

    def test_dictionary_element_and_attributes(self):
        # root tag must be 'dictionary'
        self.assertEqual(Dictionary.DICTIONARY_TAG, self.DICTIONARY.tag, "root element must be 'dictionary'")
        # must have a "title" attribute
        self.assertIsNotNone(self.DICTIONARY.title, "dictionarymust have title")
        # title value must be "simple"
        self.assertEqual(self.DICTIONARY.title, "simple", "dictionary title must be filename-base")
        # xml:lang is allowed
        print("lang: ", self.DICTIONARY.xml_lang)
        # no other attributes
        attribute_set = self.DICTIONARY.attributes_set
        unknown_attributes = Dictionary.ALLOWED_ATTRIBUTES



#    test_read_dictionary()
if __name__ == '__main__':
    unittest.main()
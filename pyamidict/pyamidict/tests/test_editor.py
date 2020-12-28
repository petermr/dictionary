# reading tests

# this works in PyCharm
from pyamidict.editor.dict import Dictionary

# this is the required syntax but fails in PyCharm and python interpreter
#from ..editor.dict import Dictionary

import os
import unittest
import xml.etree
from xml.etree import ElementTree

# have not managed to import xml schema BUG
# from xmlschema import Xml

class TestEditor(unittest.TestCase):
    RESOURCES = "resources"
    RESOURCE_DIR = os.path.join("..", RESOURCES)
    simple_xml_file = os.path.join(RESOURCE_DIR, "simple.xml")

    print("start test_editor")
    def setUp(self):
        self.root_element = Dictionary.read_dictionary_element(self.simple_xml_file)
        self.simple_dictionary = Dictionary.read_dictionary(self.simple_xml_file)

    def test_read_dictionary(self):
        text = Dictionary.read_dictionary_as_text(self.simple_xml_file)
        self.assertIsNotNone(text)
        expectedText = """<dictionary title="simple" xmlns:xml="http://www.w3.org/XML/1998/namespace">
  <metadata date="2020-08-09" source="AMI kangaroo">simple</metadata>
  <entry id="oldID" id_p297_country="AF" description="sovereign state situated at the confluence of Western, Central, and South Asia" name="Afghanistan" term="Afghanistan" wikidataURL="http://www.wikidata.org/entity/Q889" wikipediaPage="https://en.wikipedia.org/wiki/Afghanistan" wikipediaURL="https://en.wikipedia.org/wiki/Afghanistan" wikidataID="Q889">
    <synonym xml:lang='None'>AFG</synonym>
    <synonym xml:lang='None'>af</synonym>
    <synonym xml:lang='en'>Islamic Republic of Afghanistan</synonym>
    <description xml:lang='en'>sovereign state situated at the confluence of Western, Central, and South Asia</description>
  </entry>
</dictionary>
"""
        root = Dictionary.read_dictionary_element(self.simple_xml_file)
        self.assertIsNotNone(root)

        # root tag must be 'dictionary'
        self.assertEqual(root.tag, "dictionary", "root element must be 'dictionary'")

# this might vary
        self.maxDiff = None
        self.assertEqual(text, expectedText, "bad text content")

    def test_create_dictionary(self):
        self.DICTIONARY = Dictionary.read_dictionary(self.simple_xml_file)

    """
    @unittest.skip("PMR haven't manged to link in xmlschema yet ")
    def test_validate_dictionary(self):
#        import xmlschema
        xmlschema.validate('doc.xml', 'some.xsd')
    """

    @unittest.skip("not yet written")
    def test_dictionary_element_and_attributes(self):
        # must have a "title" attribute
        self.assertIsNotNone(self.simple_dictionary.title, "dictionary must have title")
        # title value must be "simple"
        self.assertEqual(self.simple_dictionary.title, "simple", "dictionary title must be filename-base")
        # xml:lang is allowed
        print("lang: ", self.simple_dictionary.xml_lang)
        # no other attributes
        attribute_set = self.simple_dictionary.attributes_set
        unknown_attributes = Dictionary.ALLOWED_ATTRIBUTES

print("test dictionary")

#    test_read_dictionary()
if __name__ == '__main__':
    unittest.main()
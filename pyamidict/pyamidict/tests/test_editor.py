# reading tests

from pyamidict.editor.dict import Dictionary
import os
import unittest
import xml.etree.ElementTree as ET

class TestEditor(unittest.TestCase):

    def setUp(self):
        self.RESOURCE_DIR = os.path.join("..", "resources")
        self.SIMPLE_XML_FILE = os.path.join(self.RESOURCE_DIR, "simple.xml")

    def test_read_dictionary(self):
#        print("dir for ed", dir(read))
        text = Dictionary.read_dictionary_as_text(self.SIMPLE_XML_FILE)
#        print(text)
        expected = """<dictionary title="simple" xmlns:xml="http://www.w3.org/XML/1998/namespace">
  <metadata date="2020-08-09" source="AMI kangaroo">simple</metadata>
  <entry id="oldID" name="simple1" term="simple1" description="simple1" wikidataID="foo" wikidataURL="https://"
         wikipediaPage="foo" wikipediaURL="https://" source="SPARQL query">
    <synonym xml:lang="en">very simple</synonym>
  </entry>
</dictionary>
"""

        self.assertEqual(expected, text)

    def test_read_dictionary_XML(self):
        root = Dictionary.read_dictionary_element(self.SIMPLE_XML_FILE)
        self.assertIsNotNone(root)

    def test_create_dictionary(self):
        pass

    def test_dictionary_attributes(self):
        root = Dictionary.read_dictionary_element(self.SIMPLE_XML_FILE)
        dictionary = Dictionary.read_dictionary(self.SIMPLE_XML_FILE)
        # root tag must be 'dictionary'
        self.assertEqual(Dictionary.DICTIONARY_TAG(), root.tag, "root element must be 'dictionary'")
        # must have a "title" attribute
        self.assertIsNotNone(root.attrib["title"], "must have title")
        # value must be "simple"
        self.assertEqual("simple", root.attrib["title"])



#    test_read_dictionary()
if __name__ == '__main__':
    unittest.main()
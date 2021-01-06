# reading tests

# this is the required syntax but fails in PyCharm and python interpreter
from bootstrap.bootstrap import Boo

import os
import unittest
import xml.etree
from xml.etree import ElementTree

# have not managed to import xml schema BUG
# from xmlschema import Xml


class TestEditor(unittest.TestCase):
    from bootstrap.stuff import Stuff

    def main():
        print("Tests on Stuff and Boo():\n%s\n%s" % (Stuff, Boo()))

    simple_xml_file = os.path.join(Stuff.RESOURCE_DIR, "simple.xml")
    print("simple_xml size", os.stat(simple_xml_file).st_size)

    print("start test_editor")
    def setUp(self):
#        print("max diff", self.maxDiff)
#        print("reading", self.simple_xml_file)
        self.root_element = Dictionary.read_dictionary_element(self.simple_xml_file)
        self.simple_dictionary = Dictionary.read_dictionary(self.simple_xml_file)

    def test_arith(self):
        self.assertEqual(2, 1+3)

    def test_read_dictionary(self):
        text = Dictionary.read_dictionary_as_text(self.simple_xml_file)
        self.assertIsNotNone(text)
        expectedText = self.SIMPLE_XML
        # file exists and is XML
        raw_root = Dictionary.read_dictionary_element(self.simple_xml_file)
        self.assertIsNotNone(raw_root, self.simple_xml_file + " must be readable XML file")

        # root tag must be 'dictionary'
        self.assertEqual(raw_root.tag, "dictionary", "root element must be 'dictionary'")

        self.maxDiff = None # (or a number)
        # raw element must be ET.Element
        self.assertEqual(str(raw_root.__class__), "<class 'xml.etree.ElementTree.Element'>", "bad raw class ")

        expected = dict(title="simple")
        self.assertEqual(raw_root.attrib, expected)


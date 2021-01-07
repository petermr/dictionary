# reading tests

# this does not work in PyCharm
from tests.schematron_test import validation

# this is the required syntax but fails in PyCharm and python interpreter
from editor.amidict import Dictionary

import os
import unittest
import xml.etree
from xml.etree import ElementTree

# have not managed to import xml schema BUG
# from xmlschema import Xml

class TestEditor(unittest.TestCase):
    # TEST CONSTANTS
    SIMPLE_XML = """<dictionary title="simple" xmlns:xml="http://www.w3.org/XML/1998/namespace">
      <metadata date="2020-08-09" source="AMI kangaroo">simple</metadata>
      <entry id="oldID" id_p297_country="AF" description="sovereign state situated at the confluence of Western, Central, and South Asia" name="Afghanistan" term="Afghanistan" wikidataURL="http://www.wikidata.org/entity/Q889" wikipediaPage="https://en.wikipedia.org/wiki/Afghanistan" wikipediaURL="https://en.wikipedia.org/wiki/Afghanistan" wikidataID="Q889">
        <synonym xml:lang='None'>AFG</synonym>
        <synonym xml:lang='None'>af</synonym>
        <synonym xml:lang='en'>Islamic Republic of Afghanistan</synonym>
        <description xml:lang='en'>sovereign state situated at the confluence of Western, Central, and South Asia</description>
      </entry>
    </dictionary>
    """

    PYAMIDICT = os.path.normpath(os.path.join(__file__, "..", ".."))
    RESOURCE_DIR = os.path.join(PYAMIDICT, "resources")

    simple_xml_file = os.path.join(RESOURCE_DIR, "simple.xml")
    print("size", os.stat(simple_xml_file).st_size)

    print("start test_editor")
    def setUp(self):
#        print("max diff", self.maxDiff)
#        print("reading", self.simple_xml_file)
        dictionary = Dictionary()
        self.root_element = dictionary.read_dictionary_element(self.simple_xml_file)
        self.simple_dictionary = dictionary.read_dictionary(self.simple_xml_file)

    def test_read_dictionary(self):
        """
        Tests reading a dictionary from its XML representation
        """
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


    def test_create_dictionary(self):
        # test
        from xml.etree import ElementTree
        root = ElementTree.parse(self.simple_xml_file).getroot()
        c = ElementTree.Element("c")
        c.text = "3"

        root.insert(1, c)
        ElementTree.dump(root)
        print("TEST")

        dictionary = Dictionary.read_dictionary(self.simple_xml_file)
        mydata = ElementTree.tostring(dictionary)
        print("mydata", dictionary.__class__, dictionary.attrib, mydata )
        file = os.path.join(os.path.expanduser("~"), "misc/junk.xml")
        print("dump to", file)
        dictionary.dumpxx(file)
        print("B=========A")

        # root element must be Dictionary object
        self.assertEqual(str(dictionary.__class__), "<class 'pyamidict.editor.amidict.Dictionary'>", "bad root class ")
        print("X=========Y")
        # Dictionary must have attributes copied from simple.xml
        expected = dict(title="simple")
        print("dict attribs", dictionary.attrib)
        self.assertEqual(dictionary.attrib, expected, "dictionary attribs")


#    @unittest.skip("PMR haven't manged to link in xmlschema yet ")
#    def test_validate_dictionary(self):
#        import xmlschema
#        xmlschema.validate('doc.xml', 'some.xsd')

#    @unittest.skip("not yet written")
    def test_dictionary_element_and_attributes(self):
        # must have a "title" attribute
        self.assertIsNotNone(self.simple_dictionary.title, "DIC001: dictionary must have title")
        # title value must be "simple"
        self.assertEqual(self.simple_dictionary.title, "simple", "DIC002: dictionary title must be filename-base")
        # xml:lang MAY be present
        print("lang: ", self.simple_dictionary.xml_lang)
        # no other attributes
        attribute_set = self.simple_dictionary.attributes_set
        unknown_attributes = Dictionary.ALLOWED_ATTRIBUTES

print("test dictionary")

#    test_read_dictionary()
if __name__ == '__main__':
    unittest.main()

class TestXML(unittest.TestCase):
    pass
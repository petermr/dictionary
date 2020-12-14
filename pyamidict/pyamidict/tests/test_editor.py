# reading tests

#from .. import top
#from ..editor import editor as ed
from pyamidict.editor import read
import os
import unittest

class TestStringMethods(unittest.TestCase):

    def test_read_dictionary(self):
        print("dir for ed", dir(read))
        simple_xml = os.path.join("..", "resources", "simple.xml")
        text = read.read_dictionary_as_text(simple_xml)
        print(text)
        expected = """<dictionary title="simple" xmlns:xml="http://www.w3.org/XML/1998/namespace">
  <desc>simple</desc>
  <entry name="simple1" term="simple1" description="simple1">
    <synonym xml:lang="en">very simple</synonym>
  </entry>
</dictionary>
"""
        self.assertEqual(expected, text)

#    test_read_dictionary()
if __name__ == '__main__':
    unittest.main()
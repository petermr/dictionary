import unittest

class TestDictionaryMethods(unittest.TestCase):
    from amidict import Dictionary
    def test_read(self):
        dict = Dictionary()
        print ("dict methods", dir(dict))
#        dictionary.read("/Users/pm286/dictionary/openVirus202011/country/country.xml")

if __name__ == '__main__':
    unittest.main()

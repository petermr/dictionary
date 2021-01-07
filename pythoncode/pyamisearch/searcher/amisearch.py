# pyamidict.editor.amisearch.py

"""
Search tool using dictionaries
"""

from ...pyamidict.editor.amidict import Dictionary

class AMISearch():

    def __init__(self):
        pass

    def add_dictionary(self, file):
        d = Dictionary(file)
        self.dictionaries.add(d)

    def remove_dictionary(self, dictionary):
        self.dictionaries.remove(dictionary)

    def search_segment_with_dict(self, dikt, segment):
        print("searching segment {} with dict {} ", segment, dikt.title)

    def search_segments_with_dict(self, dikt, segments):
        print("searching segments with dict: ", dikt.title)
        for segment in segments:
            self.search_segment_with_dict(dikt, segment)

    def search_segment(self, segment):
        for dikt in self.dictionaries:
            self.search_segment_with_dict(dikt, segment)

    def search_document(self, document):
        segments = document.get_segments()
        for segment in segments:
            self.search_segment(segment)

def Document():
    pass

def Segment():
    pass

if __name__ == "__main__":
    PYAMIDICT, RESOURCE_DIR, DICT202011 = Dictionary.get_resources()
    print("dict", Dictionary.COUNTRY_DICT)
    document = Document(os.path.join(DICT202011, ))
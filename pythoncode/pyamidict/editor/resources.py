# resources
"""
manages filenames for dictionaries and other filestore
"""
import os
from pathlib import Path

DICTIONARY_VERSION = "dictionary_version"
DICTIONARY_TOP = "dictionary_top"
DICTIONARY_DIR = "dictionary_dir"
PYAMIDICT = "pyamidict"
RESOURCE_DIR = "resources"
RESOURCES = "resources"
TEMP = "temp"

DICTIONARY_VERSIONS = {
    "cevopen",
    "openVirus202009",
    "openVirus202011",
    "openVirus20210120",
}

class Resources():

    def __init__(self):
        print("file", __file__)
        self.resource_dict = self.get_resource_dict()

    def get_resource(self, name, *, must_exist=True):
        if name not in self.resource_dict:
            print("Cannot find name in resources", name)
            return None
        p = os.path.abspath(self.resource_dict[name])
        if must_exist and not os.path.exists(p):
            print("path doesn't exist", name, p)
            return None
        return p

    @staticmethod
    def path_exists(path):
        p = Path(path).resolve()
        print(p)
        return os.path.exists(p)

    def test(self):
        n = self.get_resource(RESOURCE_DIR)
#        p = os.path(n)
        print(RESOURCE_DIR, ":", n, type(n))

    def get_paths(self, must_exist):
        return [
            self.get_resource(PYAMIDICT, must_exist=must_exist),
            self.get_resource(RESOURCE_DIR, must_exist=must_exist),
            self.get_resource(TEMP, must_exist=must_exist),
            self.get_resource(DICTIONARY_TOP, must_exist=must_exist),
            self.get_resource(DICTIONARY_DIR, must_exist=must_exist),
        ]

    def get_resource_dict(self, dictionary_version="openVirus20210120"):
        print("get_resource_dict")
        if dictionary_version not in DICTIONARY_VERSIONS:
            print("Cannot find dictionary version in ", DICTIONARY_VERSIONS)
            return None
        # these are the top/reference dirs
        pyamid = os.path.abspath(os.path.join(__file__, "..", ".."))
        dicttop = os.path.abspath(os.path.join(pyamid, "..", ".."))

        self.resource_dict = {
            PYAMIDICT : pyamid,
            RESOURCE_DIR : os.path.abspath(os.path.join(pyamid, RESOURCES)),
            TEMP : os.path.abspath(os.path.join(pyamid, TEMP)),
            DICTIONARY_TOP : dicttop,
            DICTIONARY_DIR : os.path.normpath(os.path.join(dicttop, dictionary_version))
        }
#        print("resource_dict", self.resource_dict)
        return self.resource_dict

def main():
    """
    return
    """
    res = Resources()
    res.get_paths(True)
    res.test()

#========================

if __name__ == "__main__":
    main()
else:
    main()


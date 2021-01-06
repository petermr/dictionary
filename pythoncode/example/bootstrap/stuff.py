# -*- coding: utf-8 -*-

"""bootstrap.stuff: stuff module within the bootstrap package."""
import os

class Stuff(object):
    pass

    PYAMIDICT = os.path.normpath(os.path.join(__file__, "..", "..", "..", "pyamidict"))
    print("pyamidict", PYAMIDICT)
    RESOURCE_DIR = os.path.join(PYAMIDICT, "resources")
    assert(os.path.exists(PYAMIDICT))

    simple_xml_file = os.path.join(RESOURCE_DIR, "simple.xml")
    assert(os.path.exists(simple_xml_file))
    assert(len(simple_xml_file) == 65)

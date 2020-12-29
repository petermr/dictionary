# pyamidict/example_package/subpackage1/moduleX.py
# see https://docs.python.org/3/reference/import.html
# the imports below are taken exactly from this reference

# this works in PyCharm  but not python interpreter
"""
from pyamidict.example_package.subpackage1.moduleY import yy
from pyamidict.example_package.subpackage1.moduleY import yy as yyy
from pyamidict.example_package.subpackage1 import moduleY
from pyamidict.example_package.subpackage1 import moduleY
from pyamidict.example_package.subpackage2.moduleZ import zz
from pyamidict.example_package.moduleA import aa
"""

# this SHOULD work but doesn't in either PyCharm or interpreter
from .moduleY import yy
from .moduleY import yy as yyy
from . import moduleY
from ..subpackage1 import moduleY
from ..subpackage2.moduleZ import zz
from ..moduleA import aa

def xx():
    print("xx")

yy()
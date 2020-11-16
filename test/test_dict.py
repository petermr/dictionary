# test dictiomaries and dictiomary software

from pathlib import Path
from lxml import etree
from io import StringIO
import os

def get_dictionary_dir():
    print("running dictionary_dir")
    HOME = str(Path.home())
    # will need changing per user
    dictionary_dir = os.path.join(HOME, "dictionary")
    assert os.path.exists(dictionary_dir)
    return dictionary_dir

def get_openvirus_dict_dir():
    print("running open_virus_dict_dir")
    dictionary_dir = get_dictionary_dir()
    open_virus_dir = os.path.join(dictionary_dir, "openVirus")
    assert os.path.exists(open_virus_dir)
    return open_virus_dir

def get_test_dir():
    print("running test_dir")
    dictionary_dir = get_dictionary_dir()
    test_dir = os.path.join(dictionary_dir, "test")
    assert os.path.exists(test_dir)
    return test_dir

def test_ill_formed():
    print("running ill_formed")
    dictionary_file = os.path.join(get_openvirus_dict_dir(), "bad.xml")
    assert dictionary_file != None
    try:
        etree.parse(dictionary_file)
        assert False
    except Exception as e:
        print("expected illformed: ", e)
        assert True

def test_well_formed():
    print("running well_formed")

def test_schema():
# open and read schema file
    filename_xsd = os.path.join(get_dictionary_dir(), "schema", "openVirus_schema.xsd")
    with open(filename_xsd, 'r') as schema_file:
        schema_to_check = schema_file.read()

# open and read xml file
    filename_xml = os.path.join(get_test_dir(), "simple.xml")
    with open(filename_xml, 'r') as xml_file:
        xml_to_check = xml_file.read()

    xmlschema_doc = etree.parse(StringIO(schema_to_check))
    xmlschema = etree.XMLSchema(xmlschema_doc)

    # parse xml
    try:
        doc = etree.parse(StringIO(xml_to_check))
        print('XML well formed, syntax ok.')

    # check for file IO error
    except IOError:
        print('Invalid File')

    # check for XML syntax errors
    except etree.XMLSyntaxError as err:
        print('XML Syntax Error, see error_syntax.log')
        with open('error_syntax.log', 'w') as error_log_file:
            error_log_file.write(str(err.error_log))
        quit()

    except:
        print('Unknown error, exiting.')
        quit()

    # validate against schema
    try:
        xmlschema.assertValid(doc)
        print('XML valid, schema validation ok.')

    except etree.DocumentInvalid as err:
        print('Schema validation error, see error_schema.log')
        with open('error_schema.log', 'w') as error_log_file:
            error_log_file.write(str(err.error_log))
        quit()

    except:
        print('Unknown error, exiting.')
        quit()

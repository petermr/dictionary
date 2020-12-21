from lxml import etree
from lxml import isoschematron
from lxml.isoschematron import Schematron
import os

#path_for_dict='D:main_projects\\repositories\\dictionary\\openVirus202011\\disease\\disease.xml'
class validation():
  def __init__(self,schema):
    self.schema=schema
    print('')
  
  
  def validate(self,dictionarydir,dictionary):
    path_for_dict= os.path.join(dictionarydir,dictionary,f'{dictionary}.xml')
    xml_dict = etree.parse(path_for_dict)
    path_for_schema=self.schema
    with open(path_for_schema, encoding='utf-8') as f:
      xml_schema=f.read()
    schematron = Schematron(etree.XML(xml_schema),store_report = True)
    validationResult = schematron.validate(xml_dict)
    report = schematron.validation_report
    self.report=report
    self.validationResult=validationResult
  
dictionarydir=os.path.join('..','..','..','..','dictionary','openVirus202011')

my_validation=validation('openvirusschematron.xml')
test_validation=my_validation.validate(dictionarydir,'country')
print(my_validation.report)

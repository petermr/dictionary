import xmltodict
import xml.etree.ElementTree as ET
tree = ET.parse(
    "D:\main_projects\\repositories\dictionary\ethics_statement_project\\results\\rake\ethics_statement.xml")
root = tree.getroot()
for para in root.iter('entry'):
    print(para.attrib["term"])

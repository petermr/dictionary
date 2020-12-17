from lxml import etree
from lxml.isoschematron import Schematron

schematron = Schematron(etree.XML('''
<schema xmlns="http://purl.oclc.org/dsdl/schematron" >
  <pattern id="id_only_attribute">
    <title>id is the only permitted attribute name</title>
    <rule context="*">
      <assert test="not(AAA)">Must have AAA</assert> 
      <report test="@*[not(name()='idx')]">Attribute
        <name path="@*[not(name()='id')]"/> is forbidden<name/>
      </report>
    </rule>
    <rule context="AAA">
      <assert test="not(BBB)">Must have BBB</assert> 
      <report test="@*[not(name()='id')]">Attribute
        <name path="@*[not(name()='id')]"/> is forbidden<name/>
      </report>
    </rule>
  </pattern>
</schema>'''),
error_finder=Schematron.ASSERTS_AND_REPORTS)

print("g")

xml = etree.XML('''
<AAA name="aaa">
  <BBB idx="bbb"/>
  <CCC color="ccc"/>
</AAA>
''')

schematron.validate(xml)

xml = etree.XML('''
<AAA idx="aaa">
  <BBB id="bbb"/>
  <CCC/>
</AAA>
''')

schematron.validate(xml)

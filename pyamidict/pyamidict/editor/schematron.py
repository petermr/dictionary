from lxml import etree
from lxml.isoschematron import Schematron

schematron = Schematron(etree.XML('''
<schema xmlns="http://purl.oclc.org/dsdl/schematron" >
  <pattern id="id_only_attribute">
    <title>id is the only permitted attribute name</title>
    <rule context="*">
      <report test="@*[not(name()='id')]">Attribute
        <name path="@*[not(name()='id')]"/> is forbidden<name/>
      </report>
    </rule>
  </pattern>
</schema>'''),
error_finder=Schematron.ASSERTS_AND_REPORTS)

xml = etree.XML('''
<AAA name="aaa">
  <BBB id="bbb"/>
  <CCC color="ccc"/>
</AAA>
''')

schematron.validate(xml)

xml = etree.XML('''
<AAA id="aaa">
  <BBB id="bbb"/>
  <CCC/>
</AAA>
''')

schematron.validate(xml)

"""
<schema xmlns:sch="http://purl.oclc.org/dsdl/schematron" queryBinding="xslt2"
    xmlns:sqf="http://www.schematron-quickfix.com/validator/process"
    xmlns="http://purl.oclc.org/dsdl/schematron">
    <pattern>
        <rule context="end">
            <assert test=". &gt; preceding-sibling::start">The  
                end page cannot be less than the start page</assert>
        </rule>
    </pattern>
</schema>
"""
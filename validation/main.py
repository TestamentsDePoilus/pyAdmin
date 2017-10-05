from lxml import etree as ET

relaxng_doc = ET.parse('XMLModel/test.rng')
relaxng = ET.RelaxNG(relaxng_doc)

doc = ET.parse('XMLModel/testWill.xml')
print(relaxng.validate(doc))

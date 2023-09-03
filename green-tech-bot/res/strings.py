from xml.etree import ElementTree as ET

xml_tree = ET.parse('./green-tech-bot/res/strings.xml')
strings = {elem.attrib['name']: elem.text for elem in xml_tree.getroot()}

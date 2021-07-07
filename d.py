import xml.etree.ElementTree as ET
tree = ET.parse('yml.yml')
root = tree.getroot()
tag = root.tag
att = root.attrib
#Flatten XML to CSV
for child in root:
    mainlevel = child.tag
    xmltocsv = ''
    for elem in root.iter():
        if elem.tag == root.tag:
            continue
        if elem.tag == mainlevel:
            xmltocsv = xmltocsv + '\n'
        xmltocsv = xmltocsv + str(elem.tag).rstrip() + str(elem.attrib).rstrip() + ';' + str(elem.text).rstrip() + ';'
with open('yml.csv', 'w') as file:
    file.write(xmltocsv)

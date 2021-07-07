import xml.etree.ElementTree as ET
import xmltodict
import csv

# tree = ET.parse('yml.yml')
# xml_data = tree.getroot()
#
# xmlstr = ET.tostring(xml_data, encoding='utf-8', method='xml')
#
#
# data_dict = dict(xmltodict.parse(xmlstr))
with open('yml.yml', encoding='utf-8') as fd:
    data_dict = xmltodict.parse(fd.read())

keys = data_dict.keys()
keys = list(keys)
with open('saved_data.csv', 'w') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(data_dict)


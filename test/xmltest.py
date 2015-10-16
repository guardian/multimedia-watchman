__author__ = 'david_allison'
import xml.etree.ElementTree as ET
from sys import argv


#tree = ET.parse(argv[0])

tree = ET.parse('ffqueue-config.xml')

root = tree.getroot()

print root.findall(".")

print root[0][1].text


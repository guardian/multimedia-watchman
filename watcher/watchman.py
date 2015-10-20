__author__ = 'david_allison'

import xml.etree.ElementTree as ET
from sys import argv
from pprint import pprint
from watchpuppy import WatchDogBasedSystem
import signal, os
import threading
import time
from watchedfolder import WatchedFolder

folders = {}


#START MAIN
#signal.signal(signal.SIGINT, interrupt_handler)
tree = ET.parse('ffqueue-config.xml')
root = tree.getroot()

#print root.findall(".")

#print root[0][1].text


for record in tree.findall("path"):
    f=WatchedFolder(record=record)
    #folders.append(f)
    folders[f.location] = f
    print f.__unicode__()
    s = WatchDogBasedSystem(location=f.location)
    s.daemon = True
    folders[f.location].kennel = s
    s.start()
    #pprint(f)
    #pprint(f.__dict__)

while True:
    time.sleep(3600)
#pprint(folders)
__author__ = 'david_allison'

import xml.etree.ElementTree as ET
from sys import argv
from pprint import pprint
from watchpuppy import WatchDogBasedSystem
import signal, os
import threading
import time

folders = {}

class WatchedFolder(object):
    def __init__(self,record=None,location=None,debuglevel=None,polltime=None,stable_iterations=None,command=None):
        self.location=location
        self.debuglevel=debuglevel
        self.polltime=polltime
        self.stable_iterations=stable_iterations
        self.command=command
        self.description=""
        self.kennel = None

        if record is not None:
            self.location=record.attrib['location']
            self.debuglevel=self._safe_get(record, 'debuglevel')
            self.polltime=self._safe_get(record, "poll-time")
            self.description=self._safe_get(record, "desc")
            self.command=self._safe_get(record, "command") #.format(filepath="/path/to/test/file.xml")
            self.stable_iterations=self._safe_get(record, "stable-iterations")

    def __unicode__(self):
        return u'Watched folder at {0} running \'{1}\': {2}'.format(self.location,self.command,self.description)

    def _safe_get(self, record, xpath):
        try:
            return record.find(xpath).text
        except AttributeError:
            return "(not found)"


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
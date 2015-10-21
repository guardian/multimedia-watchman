__author__ = 'david_allison'

import xml.etree.ElementTree as ET
from sys import argv
from pprint import pprint
from watchpuppy import WatchDogBasedSystem
import signal, os
import threading
import time
from watchedfolder import WatchedFolder
from raven import Client as RavenClient
from tasks import get_dsn, DSNNotFound
import logging

folders = {}


#START MAIN
#signal.signal(signal.SIGINT, interrupt_handler)
tree = ET.parse('ffqueue-config.xml')
root = tree.getroot()

#print root.findall(".")

#print root[0][1].text

try:
    raven_client = RavenClient(get_dsn(tree), raise_exception=True)
except DSNNotFound:
    logging.error("No Sentry DSN in the settings file, errors will not be logged to Sentry")
    raven_client = None

for record in tree.findall("path"):
    f=WatchedFolder(record=record, raven_client=raven_client)
    #folders.append(f)
    folders[f.location] = f
    pprint(f.__dict__)
    print f.__unicode__()
    s = WatchDogBasedSystem(location=f.location, stable_time=f.stable_time)
    s.daemon = True
    folders[f.location].kennel = s
    s.start()
    #pprint(f)
    #pprint(f.__dict__)

while True:
    time.sleep(3600)
#pprint(folders)
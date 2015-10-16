__author__ = 'david_allison'

import pyinotify
from pprint import pprint

wm = pyinotify.WatchManager()  # Watch Manager
#mask = pyinotify.IN_DELETE | pyinotify.IN_CREATE  # watched events
mask = pyinotify.IN_CREATE |  pyinotify.IN_DELETE | pyinotify.IN_CLOSE_WRITE | pyinotify.IN_CLOSE_NOWRITE # watched events


class EventHandler(pyinotify.ProcessEvent):
    def __init__(self, *args, **kwargs):
        super(EventHandler, self).__init__(*args, **kwargs)

    def process_IN_CREATE(self, event):
        print "Creating:", event.pathname

    def process_IN_DELETE(self, event):
        print "Removing:", event.pathname

    def process_IN_CLOSE_WRITE(self, event):
        print "Closed:", event.pathname

    def process_IN_CLOSE_NOWRITE(self, event):
        print "Closed (no write): ", event.pathname

handler = EventHandler()

notifier = pyinotify.Notifier(wm, handler)
#wdd = wm.add_watch('/tmp', mask, rec=True)

wdd = wm.add_watch('/mnt/mac/tdtw', mask, rec=True)

notifier.loop()
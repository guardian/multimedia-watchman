__author__ = 'david_allison'

import pyinotify

wm = pyinotify.WatchManager()  # Watch Manager
#mask = pyinotify.IN_DELETE | pyinotify.IN_CREATE  # watched events
mask = pyinotify.IN_CREATE  # watched events

class EventHandler(pyinotify.ProcessEvent):
    def process_IN_CREATE(self, event):
        print "Creating:", event.pathname

    def process_IN_DELETE(self, event):
        print "Removing:", event.pathname

handler = EventHandler()
notifier = pyinotify.Notifier(wm, handler)
#wdd = wm.add_watch('/tmp', mask, rec=True)

wdd = wm.add_watch('/mnt/mac/tdtw', mask, rec=True)

notifier.loop()
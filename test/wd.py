__author__ = 'david_allison'

import sys
import time
import logging
from watchdog.observers.polling import PollingObserver
from watchdog.events import LoggingEventHandler
from watchdog.events import FileSystemEventHandler

class MyEventHandler(FileSystemEventHandler):
    def __init__(self, observer):
        self.observer = observer
 #       self.filename = filename

    def on_created(self, event):
        print "e=", event

    def on_modified(self, event):
        print "e=", event

if __name__ == "__main__":
        path = sys.argv[1]
 #       filename = sys.argv[2]
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s - %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S')
        path = sys.argv[1] if len(sys.argv) > 1 else '.'
 #       event_handler = LoggingEventHandler()

        observer = PollingObserver()
        event_handler = MyEventHandler(observer)
        observer.schedule(event_handler, path, recursive=True)
        observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()
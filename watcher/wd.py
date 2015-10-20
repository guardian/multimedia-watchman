__author__ = 'david_allison'

import sys
import time
import logging
import os
from watchdog.observers.polling import PollingObserver,PollingObserverVFS
from watchdog.events import LoggingEventHandler
from watchdog.events import FileSystemEventHandler
from tasks import action_file


wonderfullist = []



class MyEventHandler(FileSystemEventHandler):
    def __init__(self, observer):
        self.observer = observer
 #       self.filename = filename

    def on_created(self, event):
        print "e=", event

        found = 0

        if event.is_directory == False:

            cm = 0

            while cm < len(wonderfullist):

                if event.src_path in wonderfullist[cm]:
                    print "List contains", event.src_path
                    found = 1
                    del wonderfullist[cm]
                    print "Adding ", event.src_path, " to list"
                    timestamp = time.time()
                    timeint = int(timestamp)
                    wonderfullist.append([event.src_path,timeint])

                cm = cm + 1

            if found == 0 :
                print "Adding ", event.src_path, " to list"
                timestamp = time.time()
                timeint = int(timestamp)
                wonderfullist.append([event.src_path,timeint])

            print wonderfullist

    def on_modified(self, event):
        print "e=", event

        found = 0

        if event.is_directory == False:

            cm = 0

            while cm < len(wonderfullist):

                if event.src_path in wonderfullist[cm]:
                    print "List contains", event.src_path
                    found = 1
                    del wonderfullist[cm]
                    print "Adding ", event.src_path, " to list"
                    timestamp = time.time()
                    timeint = int(timestamp)
                    wonderfullist.append([event.src_path,timeint])

                cm = cm + 1

            if found == 0 :
                print "Adding ", event.src_path, " to list"
                timestamp = time.time()
                timeint = int(timestamp)
                wonderfullist.append([event.src_path,timeint])

            print wonderfullist



if __name__ == "__main__":
        path = sys.argv[1]
 #       filename = sys.argv[2]
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s - %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S')
        path = sys.argv[1] if len(sys.argv) > 1 else '.'
 #       event_handler = LoggingEventHandler()

#        observer = PollingObserver()
        observer = PollingObserverVFS(os.stat, os.listdir, polling_interval=0.8)
        event_handler = MyEventHandler(observer)
        observer.schedule(event_handler, path, recursive=True)
        observer.start()
        try:
            while True:
                print "System running"
                timestamp2 = time.time()
                timeint2 = int(timestamp2)
                print timeint2
                for item in wonderfullist:
                    print item
                    if item[1] < (timeint2 - 10):
                        print "More than ten seconds old"
                        action_file.delay(filepath=item[0])
                        #del wonderfullist[index]

                        cm = 0

                        while cm < len(wonderfullist):

                            if item[0] in wonderfullist[cm]:
                                print "List contains", item[0]
                                found = 1
                                del wonderfullist[cm]

                            cm = cm + 1

                for index, item in enumerate(wonderfullist):
                    print index, item
                for index in range(len(wonderfullist)):
                    print index
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()

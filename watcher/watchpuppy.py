__author__ = 'david_allison'

import threading
import time
from time import sleep, time
from pprint import pprint, pformat

class WatchDogBasedSystem(threading.Thread):
    import sys
    import time
    import logging
    import os

    from watchdog.events import LoggingEventHandler
    from watchdog.events import FileSystemEventHandler
    from tasks import action_file

    def __init__(self, location=None, polltime=None, *args, **kwargs):
        super(WatchDogBasedSystem, self).__init__(*args,**kwargs)
        import logging
        self.path=location
        self.polltime=polltime
        self.wonderfullist = {}
        self.poll_delay = 1

        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s - %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S')

    def run(self):
        from watchdog.observers.polling import PollingObserver,PollingObserverVFS
        import os
        from tasks import action_file

        observer = PollingObserverVFS(os.stat, os.listdir, polling_interval=0.8)
        event_handler = self.MyEventHandler(observer, list=self.wonderfullist)
        observer.schedule(event_handler, self.path, recursive=True)
        observer.start()
        try:
            while True:
                #print "System running"
                timestamp2 = time()
                timeint2 = int(timestamp2)
                #print timeint2
                for path, ts in self.wonderfullist.items():
                    pprint({path: ts})

                    if ts < (timeint2 - 10):
                        print "{0} is More than ten seconds old".format(path)
                        action_file.delay(filepath=path)
                        #del self.wonderfullist[index]
                        del self.wonderfullist[path]

                        cm = 0

                        # while cm < len(self.wonderfullist):
                        #
                        #     if item[0] in self.wonderfullist[cm]:
                        #         print "List contains", item[0]
                        #         found = 1
                        #         del self.wonderfullist[cm]
                        #
                        #     cm = cm + 1

                # for index, item in enumerate(self.wonderfullist):
                #     print index, item
                # for index in range(len(self.wonderfullist)):
                #      print index
                sleep(self.poll_delay)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()

    def __unicode__(self):
        #global path
        #path = format(self.location)
        #print path
        return u'{0}'.format(unicode(self.path))

    class MyEventHandler(FileSystemEventHandler):
        def __init__(self, observer, list=None):
            self.observer = observer
            self.wonderfullist = list
     #       self.filename = filename

        def on_created(self, event):
            import time
            print "e=", event

            found = 0

            if event.is_directory == False:

                cm = 0
                timestamp = time.time()
                timeint = int(timestamp)
                self.wonderfullist[event.src_path] = timeint

                # while cm < len(self.wonderfullist):
                #
                #     if event.src_path in self.wonderfullist[cm]:
                #         print "List contains", event.src_path
                #         found = 1
                #         del self.wonderfullist[cm]
                #         print "Adding ", event.src_path, " to list"
                #         timestamp = time.time()
                #         timeint = int(timestamp)
                #         #self.wonderfullist.append([event.src_path,timeint])
                #         self.wonderfullist[event.src_path] = timeint
                #     cm = cm + 1
                #
                # if found == 0 :
                #     print "Adding ", event.src_path, " to list"
                #     timestamp = time.time()
                #     timeint = int(timestamp)
                #     #self.wonderfullist.append([event.src_path,timeint])
                #     self.wonderfullist[event.src_path] = timeint

                print self.wonderfullist

        def on_modified(self, event):
            print "e=", event

            found = 0

            if event.is_directory == False:
                cm = 0
                timestamp = time()
                timeint = int(timestamp)
                # while cm < len(self.wonderfullist):
                #
                #     if event.src_path in self.wonderfullist[cm]:
                #         print "List contains", event.src_path
                #         found = 1
                #         del self.wonderfullist[cm]
                #         print "Adding ", event.src_path, " to list"
                #         timestamp = time.time()
                #         timeint = int(timestamp)
                #         self.wonderfullist.append([event.src_path,timeint])
                #
                #     cm = cm + 1
                #
                # if found == 0 :
                #     print "Adding ", event.src_path, " to list"
                #     timestamp = time.time()
                #     timeint = int(timestamp)
                #     self.wonderfullist.append([event.src_path,timeint])
                #if event.src_path in self.wonderfullist:

                self.wonderfullist[event.src_path] = timeint
                print self.wonderfullist


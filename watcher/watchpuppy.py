__author__ = 'david_allison'

import threading
from time import sleep, time
from pprint import pprint


class WatchDogBasedSystem(threading.Thread):
    """
    This class represents the watchfolder system based on the 3rd party WatchDog system
    """

    from watchdog.events import FileSystemEventHandler

    def __init__(self, location=None, poll_delay=1, stable_time=10, recursive=False, ignorelist=[], *args, **kwargs):
        """
        Initialise the system
        :param location: (string) Path to the directory to watch
        :param poll_delay: (int) Sleep this long (in seconds) between each poll
        :param stable_time: (int) Trigger a file when it has been stable for this many seconds
        :param args: (other arguments for threading.Thread)
        :param kwargs: (other arguments for threading.Thread)
        """
        super(WatchDogBasedSystem, self).__init__(*args,**kwargs)
        import logging
        self.path=location
        self.wonderfullist = {}
        self.poll_delay = poll_delay
        self.stable_time = stable_time
        self.recursive = recursive
        self.ignorelist = ignorelist

        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s - %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S')

    def run(self):
        """
        "Main loop" that polls the requested folder.
        Don't call this method directly,  Call WatchDogBasedSystem.start() to run it in a seperate thread.
        :return: Does not return.
        """
        from watchdog.observers.polling import PollingObserver,PollingObserverVFS
        import os
        from tasks import action_file

        observer = PollingObserverVFS(os.stat, os.listdir, polling_interval=0.8)
        event_handler = self.MyEventHandler(observer, list=self.wonderfullist, ignorelist=self.ignorelist)
        observer.schedule(event_handler, self.path, recursive=self.recursive)
        observer.start()
        try:
            while True:
                timestamp2 = time()
                timeint2 = int(timestamp2)
                for path, ts in self.wonderfullist.items():
                    pprint({path: ts})

                    if ts < (timeint2 - self.stable_time):
                        print "{0} is More than {1} seconds old".format(path, self.stable_time)
                        action_file.delay(filepath=os.path.dirname(path), filename=os.path.basename(path))
                        del self.wonderfullist[path]


                sleep(self.poll_delay)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()

    def __unicode__(self):
        return u'{0}'.format(unicode(self.path))

    class MyEventHandler(FileSystemEventHandler):
        """
        Event handler for Watchdog
        """
        def __init__(self, observer, list=None, ignorelist=[]):
            self.observer = observer
            self.wonderfullist = list
            self.ignorelist = ignorelist

        def on_created(self, event):
            """
            Triggered when a file is created
            """
            import time
            import os
            file_name, file_extension = os.path.splitext(event.src_path)
            print "e=", event

            if file_extension in self.ignorelist:
                return

            if event.is_directory == False:

                timestamp = time.time()
                timeint = int(timestamp)
                self.wonderfullist[event.src_path] = timeint

                print self.wonderfullist

        def on_modified(self, event):
            """
            Triggered when a file is modified
            """
            import os
            file_name, file_extension = os.path.splitext(event.src_path)
            print "e=", event

            if file_extension in self.ignorelist:
                return

            if event.is_directory == False:

                timestamp = time()
                timeint = int(timestamp)


                self.wonderfullist[event.src_path] = timeint
                print self.wonderfullist


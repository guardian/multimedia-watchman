import threading
from time import sleep, time
import logging

__author__ = 'david_allison'


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
        self.logger = logging.getLogger('WatchDogBasedSystem')
        self.path=location
        self.wonderfullist = {}
        self.poll_delay = poll_delay
        self.stable_time = stable_time
        self.recursive = recursive
        self.ignorelist = ignorelist

    def run(self):
        """
        "Main loop" that polls the requested folder.
        Don't call this method directly,  Call WatchDogBasedSystem.start() to run it in a seperate thread.
        :return: Does not return.
        """
        from watchdog.observers.polling import PollingObserver,PollingObserverVFS
        import os
        from tasks import action_file
        from redis import StrictRedis
        import xml.etree.cElementTree as ET
        from watcher.global_settings import CONFIG_FILE

        tree = ET.parse(CONFIG_FILE)

        try:
            password = tree.find('/global/password').text
        except StandardError as e:
            password = ""

        try:
            expire = tree.find('/global/expire').text
            expire = int(expire)
        except StandardError as e:
            expire = 360

        self.logger.info("Starting watchpuppy on {0}".format(self.path))
        observer = PollingObserverVFS(os.stat, os.listdir, polling_interval=0.8)
        event_handler = self.MyEventHandler(observer, list=self.wonderfullist, ignorelist=self.ignorelist)
        observer.schedule(event_handler, self.path, recursive=self.recursive)
        observer.start()
        blacklist = StrictRedis(password=password,db=1)

        try:
            while True:
                timestamp2 = time()
                timeint2 = int(timestamp2)
                for path, ts in self.wonderfullist.items():
                    self.logger.debug("checking {0} with time {1}".format(path,ts))
                    if ts < (timeint2 - self.stable_time):
                        self.logger.info("{0} is More than {1} seconds old, so triggering".format(path, self.stable_time))
                        if not blacklist.exists(os.path.dirname(path)+os.path.basename(path)):
                            action_file.delay(filepath=os.path.dirname(path), filename=os.path.basename(path))
                            blacklist.setnx(os.path.dirname(path)+os.path.basename(path), os.path.dirname(path)+os.path.basename(path))
                            blacklist.expire(os.path.dirname(path)+os.path.basename(path), expire)
                        else:
                            self.logger.info("System tried to trigger on {0} but was stopped by the blacklist".format(path))

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

        def generic_event(self, event, type):
            import time
            import os
            file_name, file_extension = os.path.splitext(event.src_path)
            #print "e=", event
            logging.debug("{0} event seen: {1}".format(type,unicode(event)))
            if file_extension in self.ignorelist:
                logging.debug("ignoring event as {0} is set to ignore".format(file_extension))
                return

            if event.is_directory:
                logging.debug("event is a directory {0}, ignoring".format(type))
            else:
                timestamp = time.time()
                timeint = int(timestamp)
                logging.debug("noting event for {0} at {1}".format(event.src_path,timeint))
                self.wonderfullist[event.src_path] = timeint
                #print self.wonderfullist

        def on_created(self, event):
            """
            Triggered when a file is created
            """
            return self.generic_event(event,"create")

        def on_modified(self, event):
            """
            Triggered when a file is modified
            """
            return self.generic_event(event,"modify")

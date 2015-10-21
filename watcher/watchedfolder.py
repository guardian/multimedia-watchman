__author__ = 'david_allison'

import logging

class WatchedFolder(object):
    """
    Code that handles the reading of the XML based configuration file
    """
    def __init__(self, record=None, location=None, debuglevel=None, polltime=None, stable_time=None, command=None, raven_client=None):
        """
        Method which sets default values of various paramarters
        :param record: Misc. data
        :param location: Path to monitor
        :param debuglevel: Debugging level
        :param polltime: Not used
        :param stable_time: Time in seconds to wait before processing the file
        :param command: Linux command to execute
        :param raven_client: Raven client information
        :return:
        """
        self.location=location
        self.debuglevel=debuglevel
        self.polltime=polltime
        self.stable_time=stable_time
        self.command=command
        self.description=""
        self.kennel = None

        if record is not None:
            self.location=record.attrib['location']
            self.debuglevel=self._safe_get(record, 'debuglevel')
            self.polltime=self._safe_get(record, "poll-time")
            self.description=self._safe_get(record, "desc")
            self.command=self._safe_get(record, "command")

            try:
                self.polltime = int(self.polltime)
            except TypeError as e:
                import traceback
                if raven_client:
                    raven_client.user_context(self.__dict__)
                    raven_client.captureException()
                logging.error(traceback.format_exc())
                self.polltime = 3

            try:
                self.stable_time=record.find("stable-time").text
                self.stable_time=int(self.stable_time)
            except AttributeError:
                try:
                    iterations = int(self._safe_get(record, "stable-iterations", default=3))
                except ValueError:
                    import traceback
                    if raven_client:
                        raven_client.user_context(self.__dict__)
                        raven_client.captureException()
                    logging.error(traceback.format_exc())
                    iterations = 3
                self.stable_time = int(iterations) * self.polltime

    def __unicode__(self):
        """
        Used in print a message showing the running tasks and what they are monitoring
        :return: A string with the above information in
        """
        return u'Watched folder at {0} running \'{1}\': {2}'.format(self.location,self.command,self.description)

    def _safe_get(self, record, xpath, default="(not found)"):
        """
        Method for safely loading XML without errors causing the system to stop
        :param record: Various data
        :param xpath: Xpath data
        :param default: Set to (not found)
        """
        try:
            return record.find(xpath).text
        except AttributeError:
            return default

    def verify(self):
        if self.command is None:
            raise ValueError("Invalid watchfolder: command is not set")
        if self.location is None:
            raise ValueError("Invalid watchfolder: location is not set")
        if self.polltime is None:
            raise ValueError("Invalid watchfolder: polltime is not set")
import logging
logger = logging.getLogger('WatchedFolder')

__author__ = 'david_allison'


class WatchedFolder(object):
    """
    Code that handles the reading of the XML based configuration file
    """
    def __init__(self, record=None, location=None, debuglevel=None, polltime=None, stable_time=None, commandlist=None,
                 raven_client=None, suid_cds=False, loglevel=None):
        """
        Method which sets default values of various paramarters
        :param record: Misc. data
        :param location: Path to monitor
        :param debuglevel: Debugging level
        :param polltime: Not used
        :param stable_time: Time in seconds to wait before processing the file
        :param commandlist: List of Linux commands to execute
        :param raven_client: Raven client information
        :return:
        """
        self.location=location
        self.debuglevel=debuglevel
        self.polltime=polltime
        self.loglevel=loglevel
        self.stable_time=stable_time
        self.commandlist=commandlist
        self.description=""
        self.kennel = None
        self.ignorelist = []
        self.suid_cds = suid_cds

        if record is not None:
            self.location=record.attrib['location']
            self.debuglevel=self._safe_get(record, 'debuglevel')
            self.polltime=self._safe_get(record, "poll-time")
            self.loglevel=self._safe_get(record, "log-level")
            self.description=self._safe_get(record, "desc")
            self.commandlist=self._safe_get_list(record, "command")
            self.ignorelist=self._safe_get(record,"ignore").split('|')
            self.check_cds(record)

            try:
                self.polltime = int(self.polltime)
            except TypeError:
                import traceback
                if raven_client:
                    raven_client.user_context(self.__dict__)
                    raven_client.captureException()
                logging.error(traceback.format_exc())
                self.polltime = 3
            except ValueError:
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
            except ValueError:
                import traceback
                if raven_client:
                    raven_client.user_context(self.__dict__)
                    raven_client.captureException()
                logging.error(traceback.format_exc())
                self.stable_time = 3
        logger.info("Set up {0}".format(unicode(self)))

    def check_cds(self, record):
        for cds_node in record.findall('cds'):
            if cds_node is None:
                return

            cds_cmd = {}

            for child_node in cds_node:
                cds_cmd[child_node.tag] = child_node.text

            logger.debug("CDS command parameters: {0}".format(cds_cmd))
            args = []
            for k,v in cds_cmd.items():
                args.append("--{0} {1}".format(k,v))

            if self.suid_cds:
                cds_cmd = "/usr/local/bin/suid_cds"
            else:
                cds_cmd = "/usr/local/bin/cds_run.pl"

            if self.commandlist is None:
                self.commandlist = []
            self.commandlist.append("{cmd} {args}".format(cmd=cds_cmd, args=" ".join(args)))

            logger.debug("CDS commands are {0}".format(self.commandlist))

    def __str__(self):
        return str(self.__unicode__())

    def __unicode__(self):
        """
        Used in print a message showing the running tasks and what they are monitoring
        :return: A string with the above information in
        """
        return u'Watched folder at {0} running \'{1}\': {2}'.format(self.location,self.commandlist,self.description)

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

    def _safe_get_list(self, record, xpath, default=None):
        """
        Method for safely loading XML without errors causing the system to stop
        :param record: Various data
        :param xpath: Xpath data
        :param default: Set to (not found)
        """
        rtn = []
        for node in record.findall(xpath):
            try:
                rtn.append(node.text)
            except AttributeError:
                if default is not None: rtn.append(default)
        return rtn

    def verify(self):
        if self.commandlist is None or len(self.commandlist)==0:
            raise ValueError("Invalid watchfolder: no commands are set")
        if self.location is None:
            raise ValueError("Invalid watchfolder: location is not set")
        if self.polltime is None:
            raise ValueError("Invalid watchfolder: polltime is not set")

if __name__ == "__main__":
    import xml.etree.cElementTree as ET
    from sys import argv
    from pprint import pprint
    print "Running tests on watchedfolder module"

    logging.basicConfig(level=logging.DEBUG)
    data = ET.parse(argv[1])
    for record in data.findall("path"):
        f=WatchedFolder(record=record)
        pprint(f.__dict__)
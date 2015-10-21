__author__ = 'david_allison'


class WatchedFolder(object):
    def __init__(self,record=None,location=None,debuglevel=None,polltime=None,stable_iterations=None,command=None):
        self.location=location
        self.debuglevel=debuglevel
        self.polltime=polltime
        self.stable_iterations=stable_iterations
        self.command=command
        self.description=""
        self.kennel = None

        if record is not None:
            self.location=record.attrib['location']
            self.debuglevel=self._safe_get(record, 'debuglevel')
            self.polltime=self._safe_get(record, "poll-time")
            self.description=self._safe_get(record, "desc")
            self.command=self._safe_get(record, "command") #.format(filepath="/path/to/test/file.xml")
            self.stable_iterations=self._safe_get(record, "stable-iterations")

    def __unicode__(self):
        return u'Watched folder at {0} running \'{1}\': {2}'.format(self.location,self.command,self.description)

    def _safe_get(self, record, xpath):
        try:
            return record.find(xpath).text
        except AttributeError:
            return "(not found)"

    def verify(self):
        if self.command is None:
            raise ValueError("Invalid watchfolder: command is not set")
        if self.location is None:
            raise ValueError("Invalid watchfolder: location is not set")
        if self.polltime is None:
            raise ValueError("Invalid watchfolder: polltime is not set")
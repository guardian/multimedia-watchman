from datetime import datetime
import pytz
from redis import StrictRedis
import xml.etree.cElementTree as ET
from watcher.global_settings import CONFIG_FILE
import logging


class WatchmanBlacklist(object):
    def __init__(self, config_xml = None, location=None, loglevel=None):
        self.logger = logging.getLogger('WatchmanBlacklist.{0}'.format(location))
        try:
            self.set_log_level(loglevel)
        except Exception:
            if loglevel is not None:
                logging.warning("Attempt at setting log level {0} failed.".format(loglevel))
            pass
        if config_xml is None:
            config_xml = ET.parse(CONFIG_FILE)
        #elif not isinstance(config_xml,ET.Element) and not isinstance(config_xml,ET.ElementTree):
        #    raise TypeError("config_xml must be either None or an ElementTree element")
        
        try:
            password = config_xml.find('/global/password').text
        except StandardError as e:
            password = ""

        try:
            redishost = config_xml.find('/global/redis').text
        except StandardError as e:
            redishost = "localhost"

        try:
            expire = config_xml.find('/global/expire').text
            self.expire = int(expire)
        except StandardError as e:
            self.logger.warning("No <expire> setting in the <global> section of config. Defaulting to 360s.")
            self.expire = 360

        try:
            dbnum = config_xml.find('/global/blacklistdb').text
            self._dbnum = int(dbnum)
        except StandardError as e:
            self.logger.warning("No blacklistdb setting in the <global> section of config. Defaulting to Redis database 2.")
            dbnum = 2

        self._conn = StrictRedis(host=redishost, password=password, db=dbnum)

    def set_log_level(self, level):
        level_to_set = logging.getLevelName(level)
        self.logger.setLevel(level_to_set)

    def get(self,filepath,update=True,value="(locked)"):
        """
        Check if the given path is in the blacklist, and optionally update the lock whether or not it exists
        :param filepath: file path to check
        :param update: if True, then add the filepath to the blacklist and reset the expiry counter - even if it already exists.
        :param value: value to store against the file path (typically the mtime)
        :return: value of the key or None
        """
        
        rtn = self._conn.get(filepath)
            
        #if update:
        #    self._conn.setnx(filepath, value)
        #    self._conn.expire(filepath, self.expire)

        if not self._conn.exists(filepath):
            self.logger.debug("{0} does not exist in the blacklist. Attempting to add it.".format(filepath))
            self._conn.setnx(filepath, value)
            self._conn.expire(filepath, self.expire)
        
        return rtn
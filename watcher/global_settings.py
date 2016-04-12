__author__ = 'david_allison'
import logging

CONFIG_FILE="/etc/ffqueue-config.xml"
LOGFORMAT = '%(asctime)-15s - [%(filename)s] %(threadName)s %(funcName)s: %(levelname)s - %(message)s'
LOGFORMAT_RUNNER = '%(asctime)-15s - [%(filename)s] %(threadName)s %(funcName)s: %(levelname)s - (%(watchfolder)s) %(message)s'
LOGLEVEL = logging.DEBUG
LOGFILE = "/var/log/watchman/watchman.log"

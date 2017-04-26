#!/usr/bin/env python

WATCHMAN_VERSION = "1.4"
from shutil import copy
import os, errno
from setuptools import setup, find_packages

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise

setup(name='Watchman',
      version='1.0',
      description='A system which watches folders and executes commands when files are created in the folders',
      author='Andy Gallagher and David Allison',
      author_email='multimediatech@theguardian.com',
      packages=['watcher'],
      scripts=['watcher/watchman'],
      install_requires=['celery', 'certifi', 'raven', 'redis', 'watchdog', 'beatcop'],
      # data_files=[
      #   ('/etc', ['watcher_config/supervisord.conf']),
      #   ('/etc/init.d', ['watcher_config/initscript/supervisor']),
      #   ('/etc/supervisor/conf.d', ['watcher_config/watchman.conf']),
      #   ('/etc/sysconfig', ['watcher_config/initscript/supervisord']),
      #   ('/etc', ['watcher_config/example_config.xml'])
      #   ]
     )
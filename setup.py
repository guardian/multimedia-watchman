#!/usr/bin/env python

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
      install_requires=['celery', 'certifi', 'raven', 'redis', 'watchdog'],
      data_files=[
        # ('watcher_config/supervisord.conf', '/etc/supervisord.conf'),
        # ('watcher_config/initscript/supervisor', '/etc/init.d/supervisor'),
        # ('watcher_config/watchman.conf', '/etc/supervisor/conf.d/watchman.conf')
        ('/etc', ['watcher_config/supervisord.conf']),
        ('/etc/init.d', ['watcher_config/initscript/supervisor']),
        ('/etc/supervisor/conf.d', ['watcher_config/watchman.conf']),
        ('/etc/sysconfig', ['watcher_config/initscript/supervisord']),
        ('/etc', ['watcher_config/example_config.xml'])
        ]
     )

# if __name__ == 'main':
#     from sys import argv
#     if argv[0] != 'install':
#         exit(0)
#
#     print "--------------------------"
#     print "Creating service account..."
#     os.system('useradd -D celery')
#     print "Ensuring paths exist..."
#     mkdir_p('/var/log/watchman')
#     os.system('chown celery /var/log/watchman')
#     print "Installing configuration files..."
#     mkdir_p('/etc/supervisor/conf.d')
#     copy('watchman.conf','/etc/supervisor/conf.d/watchman.conf')
#     copy('supervisord.conf','/etc/supervisord.conf')
#     copy('initscript/supervisor','/etc/init.d')
#     print "--------------------------"
#     print "All done. Run: service supervisor start as root to initialise the system. Logs are in /var/log/watchman."
#!/usr/bin/env python

from distutils.core import setup
from shutil import copy
import os, errno

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise

setup(name='Watchman',
      version='0.31',
      description='A system which watches folders and executes commands when files are created in the folders',
      author='Andy Gallagher and David Allison',
      author_email='multimediatech@theguardian.com',
      packages=['watcher'],
      scripts=['watcher/watchman'],
      requires=['celery', 'certifi', 'raven', 'watchdog', 'supervisor']
     )

print "--------------------------"
print "Creating service account..."
os.system('useradd -D celery')
print "Ensuring paths exist..."
mkdir_p('/var/log/watchman')
os.system('chown celery /var/log/watchman')
print "Installing configuration files..."
mkdir_p('/etc/supervisor/conf.d')
copy('watchman.conf','/etc/supervisor/conf.d/watchman.conf')
copy('supervisord.conf','/etc/supervisord.conf')
copy('initscript/supervisor','/etc/init.d')
print "--------------------------"
print "All done. Run: service supervisor start as root to initialise the system. Logs are in /var/log/watchman."
#!/usr/bin/env python

from distutils.core import setup

setup(name='Watchman',
      version='0.2',
      description='A system which watches folders and executes commands when files are created in the folders',
      author='Andy Gallagher and David Allison',
      author_email='multimediatech@theguardian.com',
      packages=['watcher'],
      scripts=['watcher/watchman'],
      requires=['celery', 'certifi', 'raven', 'watchdog']
     )
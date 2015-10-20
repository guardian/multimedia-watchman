#from __future__ import absolute_import
__author__ = 'david_allison'

from celery_app import app
import logging

logger = logging.getLogger('watchman.tasks')

@app.task
def add(x, y):
    return x + y


@app.task
def mul(x, y):
    return x * y


@app.task
def xsum(numbers):
    return sum(numbers)

@app.task
def action_file(filepath="", filename=""):
    from time import sleep
    import xml.etree.cElementTree as ET
    from watchedfolder import WatchedFolder
    import os.path
    from subprocess import call

    tree = ET.parse('ffqueue-config.xml')
    #root = tree.getroot()
    config = WatchedFolder(record=tree.find('//path[@location="{0}"]'.format(filepath)))
    logger.info("config is: {0}".format(config.__dict__))
    cmd = config.command.format(pathonly=filepath, filename=filename, filepath=os.path.join(filepath, filename))
    logger.info("command to run: {0}".format(cmd))
    call(format(cmd), shell=True)

    sleep(5)
#from __future__ import absolute_import

from celery_app import app
import logging

logger = logging.getLogger('watchman.tasks')

__author__ = 'david_allison'

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
    logger.info("Got {0} {1}".format(filepath, filename))
    sleep(5)
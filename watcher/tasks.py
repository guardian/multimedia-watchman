#from __future__ import absolute_import

from celery_app import app

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
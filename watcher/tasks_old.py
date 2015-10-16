__author__ = 'david_allison'

from celery import Celery

BROKER_URL = '***REMOVED***'

CELERY_RESULT_BACKEND = '***REMOVED***'


#app = Celery('tasks', broker='***REMOVED***')
app = Celery('tasks', backend=CELERY_RESULT_BACKEND, broker=BROKER_URL)


@app.task
def add(x, y):
    return x + y
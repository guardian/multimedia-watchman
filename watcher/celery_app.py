from __future__ import absolute_import

from celery import Celery
"""
Various setting for Celery
"""

__author__ = 'david_allison'

BROKER_URL = '***REMOVED***'
CELERY_RESULT_BACKEND = '***REMOVED***'


app = Celery('watcher',
             broker=BROKER_URL,
             backend=CELERY_RESULT_BACKEND,
             include=['watcher.tasks'])

# Optional configuration, see the application user guide.
app.conf.update(
    CELERY_TASK_RESULT_EXPIRES=3600,
    CELERY_ACCEPT_CONTENT=['json'],
    CELERY_TASK_SERIALIZER='json'
)


if __name__ == '__main__':
    app.start()
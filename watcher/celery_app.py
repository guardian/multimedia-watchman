from __future__ import absolute_import

from celery import Celery

__author__ = 'david_allison'

BROKER_URL = '***REMOVED***'
CELERY_RESULT_BACKEND = '***REMOVED***'
#BROKER_URL = 'redis://localhost:6379/0'
#CELERY_RESULT_BACKEND = 'redis://localhost:6379/1'

app = Celery('watcher',
             broker=BROKER_URL,
             backend=CELERY_RESULT_BACKEND,
             include=['tasks'])

# Optional configuration, see the application user guide.
app.conf.update(
    CELERY_TASK_RESULT_EXPIRES=3600,
)

if __name__ == '__main__':
    app.start()
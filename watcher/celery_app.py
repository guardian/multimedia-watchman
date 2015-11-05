from __future__ import absolute_import

from celery import Celery
import xml.etree.cElementTree as ET
from watcher.global_settings import CONFIG_FILE

"""
Various setting for Celery
"""

__author__ = 'david_allison'

tree = ET.parse(CONFIG_FILE)

try:
    broker_url = tree.find('/global/broker-url').text
except StandardError as e:
    print "ERROR: Unable to get <broker-url> from the <global> section of {0}. Please set this and then start again.".format(CONFIG_FILE)
    exit(1)

result_backend = None
try:
    result_backend = tree.find('/global/result-backend').text
except StandardError as e:
    print "WARNING: No <result-backend> specified in the <global> section of {0}".format(CONFIG_FILE)

app = Celery('watcher',
             broker=broker_url,
             backend=result_backend,
             include=['watcher.tasks'])

# Optional configuration, see the application user guide.
app.conf.update(
    CELERY_TASK_RESULT_EXPIRES=3600,
    CELERY_ACCEPT_CONTENT=['json'],
    CELERY_TASK_SERIALIZER='json',
    #see http://docs.celeryproject.org/en/latest/configuration.html#std:setting-CELERYD_PREFETCH_MULTIPLIER
    CELERYD_CONCURRENCY=20,
    CELERYD_PREFETCH_MULTIPLIER=1,
)


if __name__ == '__main__':
    app.start()
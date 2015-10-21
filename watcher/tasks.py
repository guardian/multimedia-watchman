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


class DSNNotFound(Exception):
    pass


def get_dsn(settingsdoc, raise_exception=False):
    """
    Retrieves the global/raven-dsn setting from the settings XML
    :param settingsdoc: parsed element tree
    :return: the DSN string or None if it's not found
    """
    try:
        return settingsdoc.find('/global/raven-dsn').text
    except AttributeError:
        if raise_exception:
            raise DSNNotFound
        else:
            return None

@app.task
def action_file(filepath="", filename=""):
    from time import sleep
    import xml.etree.cElementTree as ET
    from watchedfolder import WatchedFolder
    import os.path
    from subprocess import call,check_output,CalledProcessError
    import subprocess
    from raven import Client
#    import subprocess


    tree = ET.parse('ffqueue-config.xml')
    #root = tree.getroot()
    try:
        raven_client = Client(get_dsn(tree), raise_exception=True)
    except DSNNotFound:
        logger.error("No Sentry DSN in the settings file, errors will not be logged to Sentry")
        raven_client = None

    config = WatchedFolder(record=tree.find('//path[@location="{0}"]'.format(filepath)))
    logger.info("config is: {0}".format(config.__dict__))
    cmd = config.command.format(pathonly=filepath, filename=filename, filepath=os.path.join(filepath, filename))
    logger.info("command to run: {0}".format(cmd))

    try:
        output = check_output(format(cmd), shell=True, stderr=subprocess.STDOUT)
        logger.info("output: {0}".format(output))
    except CalledProcessError as e:
        logger.error("Command {cmd} failed with exit code {code}. Output was: {out}".format(
            cmd=e.cmd,
            code=e.returncode,
            out=e.output,
        ))
        if raven_client is not None:
            raven_client.user_context({
                'triggered_path': filepath,
                'triggered_file': filename,
                'return_code': e.returncode,
                'output': e.output,
                'watcher': config.description,
            })
            raven_client.captureException()

    #e = CalledProcessError(output=output)

    sleep(5)
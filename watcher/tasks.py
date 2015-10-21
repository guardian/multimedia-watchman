__author__ = 'david_allison'

from celery_app import app
import logging

logger = logging.getLogger('watchman.tasks')

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
    """

    Submits the task to Celery, executes the Linux command, records information in the Celery log, and submits any errors to Sentry via Raven
    :param filepath: Path of the file to be acted on
    :param filename: Name of the file to be acted on
    """

    import xml.etree.cElementTree as ET
    from watchedfolder import WatchedFolder
    import os.path
    from subprocess import call,check_output,CalledProcessError
    import subprocess
    from raven import Client

    tree = ET.parse('ffqueue-config.xml')

    try:
        raven_client = Client(get_dsn(tree), raise_exception=True)
    except DSNNotFound:
        logger.error("No Sentry DSN in the settings file, errors will not be logged to Sentry")
        raven_client = None

    config = WatchedFolder(record=tree.find('//path[@location="{0}"]'.format(filepath)), raven_client=raven_client)
    logger.info("config is: {0}".format(config.__dict__))

    config.verify()

    cmd = config.command.format(pathonly=filepath, filename=filename, filepath=os.path.join(filepath, filename))
    logger.info("command to run: {0}".format(cmd))

    try:
        output = check_output(format(cmd), shell=True, stderr=subprocess.STDOUT)
        if len(output)>0:
            logger.info("output: {0}".format(unicode(output)))
        else:
            logger.info("command completed with no output")

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
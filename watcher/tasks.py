__author__ = 'david_allison'

from celery_app import app
from subprocess import CalledProcessError
import logging


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


class CommandFailed(CalledProcessError):
    """
    Upgraded eversion of CalledProcessError to hold command outputs as well
    """
    def __init__(self, stdout_text, stderr_text, *args, **kwargs):
        super(CommandFailed,self).__init__(*args,**kwargs)
        self.stdout_text = stdout_text
        self.stderr_text = stderr_text
        self.output = stderr_text + stdout_text

    def __unicode__(self):
        return u'Command {cmd} failed with output code {code}.\nStandard error: {stderr}'.format(
            cmd=self.cmd,
            code=self.returncode,
            stderr=self.stderr_text,
            stdout=self.stdout_text
        )

    def __str__(self):
        return self.__unicode__().encode('ascii')


def run_command(cmd, concat=False):
    """
    Runs the specified commandline in a shell, via subprocess
    :param cmd: Commandline to run
    :param concat:  if True, returns concatenation of standard output and standard error. If false, return a tuple.
    :return: See concat
    """
    from subprocess import Popen, PIPE
    from shlex import split

    #args = split(cmd)
    #args = ['/bin/bash', '-l', '-c', cmd]
    #logger.debug("run_command: split args are %s" % args)
    proc = Popen(cmd, shell=True, stdin=None, stdout=PIPE, stderr=PIPE)

    stdout_text, stderr_text = proc.communicate()

    if proc.returncode != 0:
        out_text = stderr_text + stdout_text
        rtn = proc.returncode
        raise CommandFailed(stdout_text, stderr_text, rtn, cmd)

    if concat:
        return stdout_text + stderr_text
    else:
        return (stdout_text, stderr_text)


class LocationConfigNotFound(StandardError):
    pass


def get_location_config(tree, loc):
    for node in tree.findall('//path'):
        if node.attrib['location'] == loc:
            return node
    raise LocationConfigNotFound(loc)

@app.task
def action_file(filepath="", filename=""):
    """

    Submits the task to Celery, executes the Linux command, records information in the Celery log, and submits any errors to Sentry via Raven
    :param filepath: Path of the file to be acted on
    :param filename: Name of the file to be acted on
    """

    import xml.etree.cElementTree as ET
    from watcher.watchedfolder import WatchedFolder
    import os.path
    from raven import Client
    from watcher.global_settings import CONFIG_FILE
    from logging import LoggerAdapter
    from global_settings import LOGFORMAT_RUNNER
    tree = ET.parse(CONFIG_FILE)

    try:
        raven_client = Client(get_dsn(tree), raise_exception=True)
    except DSNNotFound:
        logging.error("No Sentry DSN in the settings file, errors will not be logged to Sentry")
        raven_client = None

   # config = WatchedFolder(record=tree.find('//path[@location="{0}"]'.format(filepath)), raven_client=raven_client)
    use_suid_cds = False
    try:
        suid_cds = tree.find('/global/suid-cds').text
        if suid_cds.lower() != 'false':
            use_suid_cds = True
    except AttributeError:# if it's not specified, assume we're not using it.
        pass

    config = WatchedFolder(record=get_location_config(tree, filepath), raven_client=raven_client, suid_cds=use_suid_cds)

    temp = logging.getLogger('watcher.tasks')
    temp.basicConfig(format=LOGFORMAT_RUNNER)

    logger = LoggerAdapter(temp,{'watchfolder': config.description})
    logger.debug("config is: {0}".format(config.__dict__))

    config.verify()

    cmd = config.command.format(pathonly='"'+filepath+'"', filename='"'+filename+'"', filepath='"'+os.path.join(filepath, filename)+'"')
    logger.info("command to run: {0}".format(cmd))

    try:
        output = run_command(cmd, concat=True) #(format(cmd), shell=True, stderr=subprocess.STDOUT)
        if len(output)>0:
            logger.debug("output: {0}".format(unicode(output)))
        else:
            logger.debug("command completed with no output")
        logger.info("Command completed without error")

    except CommandFailed as e:
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
                'stdout': e.stdout_text,
                'stderr': e.stderr_text,
                'watcher': config.description,
                'culprit': config.description + "in run_command",
            })
            raven_client.captureMessage('{w}: Command failed with code {rtn}'.format(rtn=e.returncode,w=config.description),
                                        extra={'triggered_path': filepath,'return_code': e.returncode, 'watcher': config.description})
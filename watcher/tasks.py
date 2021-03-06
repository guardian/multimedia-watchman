__author__ = 'david_allison'

from celery_app import app
from subprocess import CalledProcessError
import logging
from threading import Thread
from datetime import datetime
import pytz


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


class ParallelExecThread(Thread):
    def __init__(self, command="",filepath="",filename="",config=None,raven_client=None,*args,**kwargs):
        super(ParallelExecThread,self).__init__(*args,**kwargs)
        self.command = command
        self.filepath = filepath
        self.filename = filename
        self.config = config
        self.raven_client=raven_client

    def run(self):
        import os.path
        cmd = self.command.format(pathonly='"'+self.filepath+'"', filename='"'+self.filename+'"', filepath='"'+os.path.join(self.filepath, self.filename)+'"')
        logging.info("({1}) command to run: {0}".format(cmd, self.config.description))

        try:
            output = run_command(cmd, concat=True) #(format(cmd), shell=True, stderr=subprocess.STDOUT)
            if len(output)>0:
                logging.debug("({1}) output: {0}".format(unicode(output), self.config.description))
            else:
                logging.debug("({0}) command completed with no output".format(self.config.description))
                logging.info("({0}) Command completed without error".format(self.config.description))

        except CommandFailed as e:
            logging.error("({d}) Command {cmd} failed with exit code {code}. Output was: {out}".format(
                d=self.config.description,
                cmd=e.cmd,
                code=e.returncode,
                out=e.output,
            ))
            if self.raven_client is not None:
                self.raven_client.user_context({
                    'triggered_path': self.filepath,
                    'triggered_file': self.filename,
                    'return_code': e.returncode,
                    'stdout': e.stdout_text,
                    'stderr': e.stderr_text,
                    'watcher': self.config.description,
                    'culprit': self.config.description + "in run_command",
                })
                self.raven_client.captureMessage('{w}: Command failed with code {rtn}'.format(rtn=e.returncode,w=self.config.description),
                                            extra={'triggered_path': self.filepath,'return_code': e.returncode, 'watcher': self.config.description})


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
    from global_settings import LOGFORMAT_RUNNER,LOGLEVEL
    from blacklist import WatchmanBlacklist
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

    blacklist = WatchmanBlacklist(config_xml=tree)

    logging.debug("Checking the blacklist for task_{0}{1}".format(filepath, filename))
    lock_ts = blacklist.get("task_"+filepath+filename)

    if lock_ts is not None:
        logging.warning("Celery tried to process "+filepath+"/"+filename+" but was stopped by the blacklist")
        #locktime = datetime.fromtimestamp(lock_ts, pytz.utc)
        #logging.warning("Celery tried to process {0} but was stopped by the blacklist from {1}".format(filepath+filename, locktime))

        return

    config = WatchedFolder(record=get_location_config(tree, filepath), raven_client=raven_client, suid_cds=use_suid_cds)

    config.verify()

    threads = []
    for command in config.commandlist:
        et = ParallelExecThread(command=command,filepath=filepath,filename=filename,config=config,raven_client=raven_client)
        et.start()
        threads.append(et)

    logging.debug("Waiting for {0} exec threads to complete".format(len(threads)))
    for et in threads:
        et.join()

from __future__ import absolute_import
import unittest2
from mock import MagicMock,patch
from os.path import abspath,basename,dirname
from pprint import pprint


class TestWatchedFolder(unittest2.TestCase):
    TEST_CONF_FILE = abspath(dirname(__file__) + "/../watcher_config/example_config.xml")

    def test_load(self):
        import xml.etree.cElementTree as ET
        from watcher.watchedfolder import WatchedFolder

        data = ET.parse(self.TEST_CONF_FILE)
        records = list(map(lambda record: WatchedFolder(record=record), data.findall("path")))

        self.assertEqual(len(records),2)
        self.assertEqual(records[0].debuglevel,"5")
        self.assertEqual(records[0].description,"Test watchfolder")
        self.assertEqual(records[0].location,"/home/watchfolders/test_one")
        self.assertEqual(records[0].polltime,5)
        self.assertEqual(records[0].stable_time,8)
        self.assertEqual(records[0].suid_cds,False)
        self.assertEqual(records[0].commandlist,['mv {filepath} /vagrant/complete;', 'sleep 2s'])

        self.assertEqual(records[1].debuglevel,"5")
        self.assertEqual(records[1].description,"Test CDS watchfolder")
        self.assertEqual(records[1].location,"/home/watchfolders/cds_test")
        self.assertEqual(records[1].polltime,5)
        self.assertEqual(records[1].stable_time,8)
        self.assertEqual(records[1].suid_cds,False)
        self.assertEqual(records[1].commandlist,['/usr/local/bin/cds_run.pl --route testroute.xml --input-inmeta {filepath}'])

        pprint(records[0].__dict__)
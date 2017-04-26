from __future__ import absolute_import
import unittest2
from mock import MagicMock,patch
from os.path import abspath,basename,dirname
from pprint import pprint
import logging

logging.basicConfig(level=logging.DEBUG)


class TestEventHandler(unittest2.TestCase):
    def test_generic_event_create_file(self):
        """
        Test that a file event is recorded
        :return:
        """
        from watcher.watchpuppy import WatchDogBasedSystem
        from watchdog.events import FileSystemEvent
        observer = MagicMock()
        list = {}

        handler = WatchDogBasedSystem.MyEventHandler(observer,list)

        mock_event = MagicMock(FileSystemEvent)
        mock_event.is_directory = False
        mock_event.src_path = "/path/to/file.ext"

        with patch("time.time",return_value=123456):
            handler.generic_event(mock_event,"create")
            self.assertDictContainsSubset({'/path/to/file.ext': 123456}, list)

    def test_generic_event_create_dir(self):
        """
        Test that a directory event is ignored
        :return:
        """
        from watcher.watchpuppy import WatchDogBasedSystem
        from watchdog.events import FileSystemEvent
        observer = MagicMock()
        list = {}

        handler = WatchDogBasedSystem.MyEventHandler(observer,list)

        mock_event = MagicMock(FileSystemEvent)
        mock_event.is_directory = True
        mock_event.src_path = "/path/to/directory"

        with patch("time.time",return_value=123456):
            handler.generic_event(mock_event,"create")
            self.assertEqual(len(list),0) #directory event should be ignored

    def test_generic_event_create_ignorelist(self):
        """
        Test that a directory event is ignored
        :return:
        """
        from watcher.watchpuppy import WatchDogBasedSystem
        from watchdog.events import FileSystemEvent
        observer = MagicMock()
        list = {}
        ignorelist = ['.ext']
        handler = WatchDogBasedSystem.MyEventHandler(observer,list,ignorelist)

        mock_event = MagicMock(FileSystemEvent)
        mock_event.is_directory = True
        mock_event.src_path = "/path/to/file.ext"

        with patch("time.time",return_value=123456):
            handler.generic_event(mock_event,"create")
            self.assertEqual(len(list),0)

    def test_oncreate(self):
        """
        Test the on_create event
        :return:
        """
        with patch('watcher.watchpuppy.WatchDogBasedSystem.MyEventHandler.generic_event') as mock_generic:
            from watcher.watchpuppy import WatchDogBasedSystem
            from watchdog.events import FileSystemEvent
            observer = MagicMock()
            list = {}

            handler = WatchDogBasedSystem.MyEventHandler(observer, list)
            mock_event = MagicMock(FileSystemEvent)
            mock_event.is_directory = True
            mock_event.src_path = "/path/to/file.ext"

            handler.on_created(mock_event)
            mock_generic.assert_called_once_with(mock_event,"create")

    def test_onmodified(self):
        """
        Test the on_modified event
        :return:
        """
        with patch('watcher.watchpuppy.WatchDogBasedSystem.MyEventHandler.generic_event') as mock_generic:
            from watcher.watchpuppy import WatchDogBasedSystem
            from watchdog.events import FileSystemEvent
            observer = MagicMock()
            list = {}

            handler = WatchDogBasedSystem.MyEventHandler(observer, list)
            mock_event = MagicMock(FileSystemEvent)
            mock_event.is_directory = True
            mock_event.src_path = "/path/to/file.ext"

            handler.on_modified(mock_event)
            mock_generic.assert_called_once_with(mock_event,"modify")
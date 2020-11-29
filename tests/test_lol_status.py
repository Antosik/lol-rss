from requests import HTTPError
import unittest
from unittest import mock

from handlers.lol.status import LoLServerStatusHandler
from tests.__mocks__.server_status import mocked_success_get
from tests.helpers.mock_response import (
    mocked_unsuccessful_get, mocked_notfound_get
)


class LoLServerStatusHanderTest(unittest.TestCase):

    def setUp(self):
        self.server = {'id': 'randomId', 'region': 'randomRegion', 'locale': 'randomLocale', 'title': 'randomTitle', 'description': 'randomDescription'}
        self.handler = LoLServerStatusHandler()

    def test_load_servers(self):
        servers = self.handler.load_servers()
        self.assertIsInstance(servers, list)

    def test_filepath(self):
        result = self.handler.get_filepath(self.server)
        self.assertEqual(result, '/lol/randomRegion/status.randomLocale.xml')

    @mock.patch('util.abstract.collector.requests.get', side_effect=mocked_success_get)
    def test_successful_fetch(self, mock_post):

        feed = self.handler.process_server(self.server)

        self.assertEqual(feed.getTitle(), 'randomTitle')
        self.assertEqual(feed.getLanguage(), 'randomLocale')
        self.assertEqual(feed.getAlternateLink(), 'https://status.riotgames.com/lol?region=randomId&locale=randomLocale')

        item = feed.getItems()[0]
        self.assertEqual(item.getTitle(), 'Random Title')
        self.assertEqual(item.getSummary(), 'Random Text')
        self.assertEqual(item.getLink(), 'https://status.riotgames.com/lol?region=randomId&locale=randomLocale&id=2')
        self.assertEqual(item.getAuthor(), 'Random Author')
        self.assertEqual(item.getCreatedAt(), '2020-11-08T01:25:00.434856+00:00')
        self.assertEqual(item.getUpdatedAt(), '2020-11-08T01:25:00.434856+00:00')

    @mock.patch('util.abstract.collector.requests.get', side_effect=mocked_unsuccessful_get)
    def test_unsuccessful_fetch(self, mock_get):

        with self.assertRaises(Exception):
            self.handler.process_server(self.server)

    @mock.patch('util.abstract.collector.requests.get', side_effect=mocked_notfound_get)
    def test_notfound_fetch(self, mock_get):

        with self.assertRaises(HTTPError):
            self.handler.process_server(self.server)

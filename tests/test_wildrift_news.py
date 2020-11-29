from requests import HTTPError
import unittest
from unittest import mock

from handlers.wildrift.news import WildRiftNewsHandler
from tests.__mocks__.wildrift_news import mocked_success_get
from tests.helpers.mock_response import (
    mocked_unsuccessful_get, mocked_notfound_get
)


class WildRiftNewsHanderTest(unittest.TestCase):

    def setUp(self):
        self.server = {'id': 'randomId', 'region': 'randomRegion', 'locale': 'randomLocale', 'title': 'randomTitle', 'description': 'randomDescription'}
        self.handler = WildRiftNewsHandler()

    def test_load_servers(self):
        servers = self.handler.load_servers()
        self.assertIsInstance(servers, list)

    def test_filepath(self):
        result = self.handler.get_filepath(self.server)
        self.assertEqual(result, '/wildrift/randomLocale/news.xml')

    @mock.patch('util.abstract.collector.requests.get', side_effect=mocked_success_get)
    def test_successful_fetch(self, mock_get):

        feed = self.handler.process_server(self.server)

        self.assertEqual(feed.getTitle(), 'randomTitle')
        self.assertEqual(feed.getLanguage(), 'randomLocale')
        self.assertEqual(feed.getAlternateLink(), 'https://wildrift.leagueoflegends.com/randomlocale/news/')

        item = feed.getItems()[0]
        self.assertEqual(item.getTitle(), 'Random Title')
        self.assertEqual(item.getSummary(), 'Random Description')
        self.assertEqual(item.getLink(), 'https://wildrift.leagueoflegends.com/randomlocale/news/random-post/')
        self.assertEqual(item.getCreatedAt().isoformat(), '2020-11-11T00:00:00+00:00')
        self.assertEqual(item.getUpdatedAt().isoformat(), '2020-11-11T00:00:00+00:00')
        self.assertEqual(item.getImage(), 'https://example.com')

    @mock.patch('util.abstract.collector.requests.get', side_effect=mocked_unsuccessful_get)
    def test_unsuccessful_fetch(self, mock_get):

        with self.assertRaises(Exception):
            self.handler.process_server(self.server)

    @mock.patch('util.abstract.collector.requests.get', side_effect=mocked_notfound_get)
    def test_notfound_fetch(self, mock_get):

        with self.assertRaises(HTTPError):
            self.handler.process_server(self.server)

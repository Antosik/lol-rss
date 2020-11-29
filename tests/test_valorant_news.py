from requests import HTTPError
import unittest
from unittest import mock

from handlers.valorant.news import ValorantNewsHandler
from tests.__mocks__.valorant_news import mocked_success_get
from tests.helpers.mock_response import (
    mocked_unsuccessful_get, mocked_notfound_get
)


class ValorantNewsHanderTest(unittest.TestCase):

    def setUp(self):
        self.server = {'id': 'randomId', 'region': 'randomRegion', 'locale': 'randomLocale', 'title': 'randomTitle', 'description': 'randomDescription'}
        self.handler = ValorantNewsHandler()

    def test_load_servers(self):
        servers = self.handler.load_servers()
        self.assertIsInstance(servers, list)

    def test_filepath(self):
        result = self.handler.get_filepath(self.server)
        self.assertEqual(result, '/valorant/randomLocale/news.xml')

    @mock.patch('util.abstract.collector.requests.get', side_effect=mocked_success_get)
    def test_successful_fetch(self, mock_get):

        feed = self.handler.process_server(self.server)

        self.assertEqual(feed.getTitle(), 'randomTitle')
        self.assertEqual(feed.getDescription(), 'randomDescription')
        self.assertEqual(feed.getLanguage(), 'randomLocale')
        self.assertEqual(feed.getAlternateLink(), 'https://playvalorant.com/randomlocale/news/')

        item = feed.getItems()[0]
        self.assertEqual(item.getTitle(), 'Random Title')
        self.assertEqual(item.getSummary(), 'Random Description')
        self.assertEqual(item.getLink(), 'https://playvalorant.com/randomlocale/news/random-post/')
        self.assertEqual(item.getCreatedAt(), '2020-11-25T12:00:00.000Z')
        self.assertEqual(item.getUpdatedAt(), '2020-11-25T12:00:00.000Z')
        self.assertEqual(item.getImage(), 'https://example.com')

    @mock.patch('util.abstract.collector.requests.get', side_effect=mocked_unsuccessful_get)
    def test_unsuccessful_fetch(self, mock_get):

        with self.assertRaises(Exception):
            self.handler.process_server(self.server)

    @mock.patch('util.abstract.collector.requests.get', side_effect=mocked_notfound_get)
    def test_notfound_fetch(self, mock_get):

        with self.assertRaises(HTTPError):
            self.handler.process_server(self.server)

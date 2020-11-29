from requests import HTTPError
import unittest
from unittest import mock

from handlers.lol.ruesports import LoLRUeSportsHandler
from tests.__mocks__.lol_ruesports import mocked_success_get
from tests.helpers.mock_response import mocked_notfound_get


class LoLRUeSportsHanderTest(unittest.TestCase):

    def setUp(self):
        self.server = {'id': 'randomId', 'region': 'randomRegion', 'locale': 'randomLocale', 'title': 'randomTitle', 'description': 'randomDescription'}
        self.handler = LoLRUeSportsHandler()

    def test_load_servers(self):
        servers = self.handler.load_servers()
        self.assertIsInstance(servers, list)

    def test_filepath(self):
        result = self.handler.get_filepath(self.server)
        self.assertEqual(result, '/lol/randomRegion/esports.randomLocale.xml')

    @mock.patch('sources.lol.ruesports.requests.post', side_effect=mocked_success_get)
    def test_successful_fetch(self, mock_post):

        feed = self.handler.process_server(self.server)

        self.assertEqual(feed.getTitle(), 'randomTitle')
        self.assertEqual(feed.getDescription(), 'randomDescription')
        self.assertEqual(feed.getLanguage(), 'randomLocale')
        self.assertEqual(feed.getAlternateLink(), 'https://ru.lolesports.com/articles/')

        item = feed.getItems()[0]
        self.assertEqual(item.getTitle(), 'Random Title')
        self.assertEqual(item.getLink(), 'https://ru.lolesports.com/articles/1')
        self.assertEqual(item.getAuthor(), 'Random Author')
        self.assertEqual(item.getCreatedAt(), '2020-11-25T17:04:11.457Z')
        self.assertEqual(item.getUpdatedAt(), '2020-11-25T17:04:11.457Z')
        self.assertEqual(item.getImage(), 'https://example.com')

    @mock.patch('sources.lol.ruesports.requests.post', side_effect=mocked_notfound_get)
    def test_notfound_fetch(self, mock_post):

        with self.assertRaises(HTTPError):
            self.handler.process_server(self.server)

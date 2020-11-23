import os

from sources.wildrift.news import WildRiftNewsCollector
from util.abstract.feed import Feed
from util.abstract.handler import Handler
from util.functions.load_json import load_json


class WildRiftNewsHandler(Handler):

    def load_servers(self):
        servers_filepath = os.path.join(os.path.dirname(__file__), '../../data/wildrift/news.json')
        return load_json(servers_filepath)

    def get_filepath(self, server):
        return '/wildrift/{locale}/news.xml'.format(locale=server['locale'])

    def process_server(self, server):
        collector = WildRiftNewsCollector(server)
        items = collector.collect()

        alternateLink = collector.construct_alternate_link() + 'news/'

        feed = Feed()
        feed.setTitle(server['title'])
        feed.setAlternateLink(alternateLink)
        feed.setLanguage(server['locale'])
        feed.setItems(items)

        return feed


def handle(event={}, context={}):
    """Handler for AWS Lambda - WildRift News"""
    WildRiftNewsHandler().run()
    return 'ok'

import os

from sources.lol.status import LOLServerStatusCollector
from util.abstract.feed import Feed
from util.abstract.handler import Handler
from util.functions.load_json import load_json


class LoLServerStatusHandler(Handler):

    def load_servers(self):
        servers_filepath = os.path.join(os.path.dirname(__file__), '../../data/lol/status.json')
        return load_json(servers_filepath)

    def get_filepath(self, server):
        return '/lol/{region}/status.{locale}.xml'.format(region=server['region'], locale=server['locale'])

    def process_server(self, server):
        collector = LOLServerStatusCollector(server)
        items = collector.collect()

        alternateLink = collector.construct_alternate_link()

        feed = Feed()
        feed.setTitle(server['title'])
        feed.setAlternateLink(alternateLink)
        feed.setLanguage(server['locale'])
        feed.setItems(items)

        return feed


def handle(event={}, context={}):
    """Handler for AWS Lambda - LoL Server Status"""
    LoLServerStatusHandler().run()
    return 'ok'

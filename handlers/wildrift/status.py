import os

from sources.wildrift.status import WildRiftServerStatusCollector
from util.abstract.feed import Feed
from util.abstract.handler import Handler
from util.functions.load_json import load_json


class WildRiftServerStatusHandler(Handler):

    def load_servers(self):

        locale_filepath = os.path.join(os.path.dirname(__file__), '../../data/wildrift/status-locales.json')
        locales = load_json(locale_filepath)

        servers_filepath = os.path.join(os.path.dirname(__file__), '../../data/wildrift/status-servers.json')
        servers = load_json(servers_filepath)

        results = []
        for locale in locales:
            for server in servers:
                results.append({'region': server['id'], 'id': server['id'], **locale})
        return results

    def get_filepath(self, server):
        return '/wildrift/{locale}/{region}.status.xml'.format(region=server['region'], locale=server['locale'])

    def process_server(self, server):
        collector = WildRiftServerStatusCollector(server)
        items = collector.collect()

        alternateLink = collector.construct_alternate_link()

        feed = Feed()
        feed.setTitle(server['title'])
        feed.setAlternateLink(alternateLink)
        feed.setLanguage(server['locale'])
        feed.setItems(items)

        return feed


def handle(event={}, context={}):
    """Handler for AWS Lambda - WildRift Server Status"""
    WildRiftServerStatusHandler().run()
    return 'ok'

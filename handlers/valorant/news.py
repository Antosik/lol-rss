import os

from sources.valorant.news import ValorantNewsCollector
from util.abstract.feed import Feed
from util.abstract.handler import Handler
from util.functions.load_json import load_json


class ValorantNewsHandler(Handler):

    def load_servers(self):
        servers_filepath = os.path.join(os.path.dirname(__file__), '../../data/valorant/news.json')
        return load_json(servers_filepath)

    def get_filepath(self, server):
        return '/valorant/{locale}/news.xml'.format(locale=server['locale'])

    def process_server(self, server):
        collector = ValorantNewsCollector(server)
        items = collector.collect()

        alternateLink = collector.construct_alternate_link() + 'news/'

        feed = Feed()
        feed.setTitle(server['title'])
        feed.setDescription(server['description'])
        feed.setAlternateLink(alternateLink)
        feed.setLanguage(server['locale'])
        feed.setItems(items)

        return feed


def handle(event={}, context={}):
    """Handler for AWS Lambda - Valorant News"""
    ValorantNewsHandler().run()
    return 'ok'

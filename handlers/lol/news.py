import os

from sources.lol.news import LOLNewsCollector
from util.abstract.feed import Feed
from util.abstract.handler import Handler
from util.functions.load_json import load_json


class LoLNewsHandler(Handler):

    def load_servers(self):
        servers_filepath = os.path.join(os.path.dirname(__file__), '../../data/lol/news.json')
        return load_json(servers_filepath)

    def get_filepath(self, server):
        return '/lol/{region}/news.{locale}.xml'.format(region=server['region'], locale=server['locale'])

    def process_server(self, server):
        collector = LOLNewsCollector(server)
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
    """Handler for AWS Lambda - LoL News"""
    LoLNewsHandler().run()
    return 'ok'

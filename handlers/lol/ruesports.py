from sources.lol.ruesports import LOLRUeSportsCollector
from util.abstract.feed import Feed
from util.abstract.handler import Handler


class LoLRUeSportsHandler(Handler):

    def load_servers(self):
        return [{
            'locale': 'ru-RU',
            'region': 'ru',
            'title': 'LoL Киберспорт',
            'description': 'Статьи и новости с ru.lolesports.com'
        }]

    def get_filepath(self, server):
        return '/lol/{region}/esports.{locale}.xml'.format(region=server['region'], locale=server['locale'])

    def process_server(self, server):
        collector = LOLRUeSportsCollector()
        items = collector.collect()

        alternateLink = collector.construct_alternate_link()

        feed = Feed()
        feed.setTitle(server['title'])
        feed.setDescription(server['description'])
        feed.setAlternateLink(alternateLink)
        feed.setLanguage(server['locale'])
        feed.setItems(items)

        return feed


def handle(event={}, context={}):
    """Handler for AWS Lambda - LoL RU Esports"""
    LoLRUeSportsHandler().run()
    return 'ok'

from __future__ import absolute_import

from sources.lol.ruesports import LOLRUeSportsCollector
from util.rss.generator import RssFeedGenerator


def handle(event={}, context={}):
    """Handler for AWS Lambda"""

    collector = LOLRUeSportsCollector()

    target_dir = '/tmp/'

    dirpath = '/lol/ru/'
    filename = 'esports.xml'
    filepath = dirpath + filename

    selflink = RssFeedGenerator.selflink_s3(filepath)
    generator = RssFeedGenerator(
        meta={
            'id': selflink,
            'title': 'LoL Киберспорт [RU]',
            'description': 'Статьи и новости с ru.lolesports.com',
            'link': [
                {
                    'href': selflink,
                    'rel': 'self'
                }, {
                    'href': 'https://ru.lolesports.com/articles',
                    'rel': 'alternate'
                }
            ],
            'author': {'name': 'Antosik', 'uri': 'https://github.com/Antosik'},
            'language': 'ru-RU',
            'ttl': 15
        },
        collector=collector
    )

    generator.generate(target_dir + filepath)
    generator.uploadToS3(target_dir + filepath, filepath[1:])

    return 'ok'

import json
import os

from sources.valorant.news import ValorantNewsCollector
from util.rss.generator import RssFeedGenerator


def handle(event={}, context={}):
    """Handler for AWS Lambda"""

    target_dir = '/tmp/'
    locales_filepath = os.path.join(os.path.dirname(__file__), '../../data/valorant/news.json')

    with open(locales_filepath, encoding="utf8") as json_file:

        locales = json.load(json_file)

        for locale in locales:

            collector = ValorantNewsCollector(locale)

            dirpath = '/valorant/{region}/'.format(region=locale['locale'])
            filename = 'news.xml'
            filepath = dirpath + filename

            selflink = RssFeedGenerator.selflink_s3(filepath)
            generator = RssFeedGenerator(
                meta={
                    'id': selflink,
                    'title': locale['title'],
                    'description': locale['description'],
                    'link': [
                        {
                            'href': selflink,
                            'rel': 'self'
                        },
                        {
                            'href': ValorantNewsCollector.construct_alternate_link(locale=locale['locale']) + 'news/',
                            'rel': 'alternate'
                        }
                    ],
                    'author': {
                        'name': 'Antosik',
                        'uri': 'https://github.com/Antosik'
                    },
                    'language': 'ru',
                    'ttl': 15
                },
                collector=collector
            )

            generator.generate(target_dir + filepath)
            generator.uploadToS3(target_dir + filepath, filepath[1:])

    return 'ok'

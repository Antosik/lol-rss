import json
import os

from sources.valorant.status import ValorantServerStatusCollector
from util.rss.generator import RssFeedGenerator


def handle(event={}, context={}):
    """Handler for AWS Lambda"""

    target_dir = '/tmp/'
    locale_filepath = os.path.join(os.path.dirname(__file__), '../../data/valorant/status.json')
    regions = ['ap', 'br', 'eu', 'kr', 'latam', 'na']

    with open(locale_filepath, encoding="utf8") as json_file:

        locales = json.load(json_file)

        for locale in locales:

            dirpath = '/valorant/{region}/'.format(region=locale['locale'])

            for region in regions:

                collector = ValorantServerStatusCollector({'region': region, 'id': region, **locale})

                filename = '{region}.status.xml'.format(region=region)
                filepath = dirpath + filename

                selflink = RssFeedGenerator.selflink_s3(filepath)
                generator = RssFeedGenerator(
                    meta={
                        'id': selflink,
                        'title': locale['title'],
                        'link': [
                            {
                                'href': selflink,
                                'rel': 'self'
                            },
                            {
                                'href': collector.construct_alternate_link(),
                                'rel': 'alternate'
                            }
                        ],
                        'author': {'name': 'Antosik', 'uri': 'https://github.com/Antosik'},
                        'language': locale['locale'],
                        'ttl': 15
                    },
                    collector=collector
                )

                generator.generate(target_dir + filepath)
                generator.uploadToS3(target_dir + filepath, filepath[1:])

    return 'ok'

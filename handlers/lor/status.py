import json
import os

from sources.lor.status import LoRServerStatusCollector
from util.rss.generator import RssFeedGenerator


def handle(event={}, context={}):
    """Handler for AWS Lambda"""

    target_dir = '/tmp/'
    locale_filepath = os.path.join(os.path.dirname(__file__), '../../data/lor/status.json')
    regions = ['americas', 'asia', 'europe', 'sea']

    with open(locale_filepath, encoding="utf8") as json_file:

        locales = json.load(json_file)

        for locale in locales:

            dirpath = '/lor/{region}/'.format(region=locale['locale'])

            for region in regions:

                collector = LoRServerStatusCollector({'region': region, 'id': region, **locale})

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

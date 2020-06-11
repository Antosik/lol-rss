import json
import os

from sources.lol.status import LOLServerStatusCollector
from util.rss.generator import RssFeedGenerator


def handle(event={}, context={}):
    """Handler for AWS Lambda"""

    target_dir = '/tmp/'
    servers_filepath = os.path.join(os.path.dirname(__file__), '../../data/lol/status.json')

    with open(servers_filepath, encoding="utf8") as json_file:

        servers = json.load(json_file)

        for server in servers:

            collector = LOLServerStatusCollector(server)

            dirpath = '/lol/{region}/'.format(region=server['region'])
            filename = 'status.xml'
            filepath = dirpath + filename

            selflink = RssFeedGenerator.selflink_s3(filepath)
            generator = RssFeedGenerator(
                meta={
                    'id': selflink,
                    'title': server['title'],
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
                    'language': server['locale'],
                    'ttl': 15
                },
                collector=collector
            )

            generator.generate(target_dir + filepath)
            generator.uploadToS3(target_dir + filepath, filepath[1:])

    return 'ok'

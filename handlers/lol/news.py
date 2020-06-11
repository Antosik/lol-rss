from __future__ import absolute_import

import json
import os

from sources.lol.news import LOLNewsCollector
from util.rss.generator import RssFeedGenerator


def handle(event={}, context={}):
    """Handler for AWS Lambda"""

    target_dir = '/tmp/'
    servers_filepath = os.path.join(os.path.dirname(__file__), '../../data/lol/news.json')

    with open(servers_filepath, encoding="utf8") as json_file:

        servers = json.load(json_file)

        for server in servers:

            collector = LOLNewsCollector(server)

            dirpath = '/lol/{region}/'.format(region=server['region'])
            filename = 'news.xml'
            filepath = dirpath + filename

            selflink = RssFeedGenerator.selflink_s3(filepath)
            generator = RssFeedGenerator(
                meta={
                    'id': selflink,
                    'title': server['title'],
                    'description': server['description'],
                    'link': [
                        {
                            'href': selflink,
                            'rel': 'self'
                        },
                        {
                            'href': LOLNewsCollector.construct_alternate_link(region=server['region'], locale=server['locale']) + 'news/',
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

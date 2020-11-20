import os

from sources.valorant.status import ValorantServerStatusCollector
from util.abstract.feed import Feed
from util.functions.load_json import load_json
from util.rss.generator import AtomGenerator
from util.s3 import S3


def handle(event={}, context={}):
    """Handler for AWS Lambda - Valorant Server Status"""

    locale_filepath = os.path.join(os.path.dirname(__file__), '../../data/valorant/status-locales.json')
    locales = load_json(locale_filepath)

    servers_filepath = os.path.join(os.path.dirname(__file__), '../../data/valorant/status-servers.json')
    servers = load_json(servers_filepath)

    target_dir = '/tmp/'
    s3 = S3()

    for locale in locales:
        for server in servers:

            filepath = '/v3/valorant/{locale}/{region}.status.xml'.format(locale=locale['locale'], region=server['id'])
            fullpath = target_dir + filepath

            collector = ValorantServerStatusCollector({'region': server['id'], 'id': server['id'], **locale})
            items = collector.collect()

            selfLink = S3.generate_link(filepath)
            alternateLink = collector.construct_alternate_link()

            feed = Feed()
            feed.generateUUID(selfLink)
            feed.setTitle(locale['title'])
            feed.setSelfLink(selfLink)
            feed.setAlternateLink(alternateLink)
            feed.setLanguage(locale['locale'])
            feed.setItems(items)

            generator = AtomGenerator(feed)
            generator.generate(fullpath)

            s3.upload(fullpath, filepath[1:])

    return 'ok'

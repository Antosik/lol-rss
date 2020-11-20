import os

from sources.lol.status import LOLServerStatusCollector
from util.abstract.feed import Feed
from util.functions.load_json import load_json
from util.rss.generator import AtomGenerator
from util.s3 import S3


def handle(event={}, context={}):
    """Handler for AWS Lambda - LoL Server Status"""

    servers_filepath = os.path.join(os.path.dirname(__file__), '../../data/lol/status.json')
    servers = load_json(servers_filepath)

    target_dir = '/tmp/'
    s3 = S3()

    for server in servers:

        filepath = '/v3/lol/{region}/status.xml'.format(region=server['region'])
        fullpath = target_dir + filepath

        collector = LOLServerStatusCollector(server)
        items = collector.collect()

        selfLink = S3.generate_link(filepath)
        alternateLink = collector.construct_alternate_link()

        feed = Feed()
        feed.generateUUID(selfLink)
        feed.setTitle(server['title'])
        feed.setSelfLink(selfLink)
        feed.setAlternateLink(alternateLink)
        feed.setLanguage(server['locale'])
        feed.setItems(items)

        generator = AtomGenerator(feed)
        generator.generate(fullpath)

        s3.upload(fullpath, filepath[1:])

    return 'ok'

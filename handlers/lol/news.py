import os

from sources.lol.news import LOLNewsCollector
from util.abstract.feed import Feed
from util.functions.load_json import load_json
from util.rss.generator import AtomGenerator
from util.s3 import S3


def handle(event={}, context={}):
    """Handler for AWS Lambda - LoL News"""

    servers_filepath = os.path.join(os.path.dirname(__file__), '../../data/lol/news.json')
    servers = load_json(servers_filepath)

    target_dir = '/tmp/'
    s3 = S3()

    for server in servers:

        filepath = '/v3/lol/{region}/news.xml'.format(region=server['region'])
        fullpath = target_dir + filepath

        collector = LOLNewsCollector(server)
        items = collector.collect()

        selfLink = S3.generate_link(filepath)
        alternateLink = collector.construct_alternate_link() + 'news/'

        feed = Feed()
        feed.generateUUID(selfLink)
        feed.setTitle(server['title'])
        feed.setDescription(server['description'])
        feed.setSelfLink(selfLink)
        feed.setAlternateLink(alternateLink)
        feed.setLanguage(server['locale'])
        feed.setItems(items)

        generator = AtomGenerator(feed)
        generator.generate(fullpath)

        s3.upload(fullpath, filepath[1:])

    return 'ok'

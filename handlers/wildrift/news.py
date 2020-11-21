import os

from sources.wildrift.news import WildRiftNewsCollector
from util.abstract.feed import Feed
from util.functions.load_json import load_json
from util.rss.generator import AtomGenerator
from util.s3 import S3


def handle(event={}, context={}):
    """Handler for AWS Lambda - WildRift News"""

    locales_filepath = os.path.join(os.path.dirname(__file__), '../../data/wildrift/news.json')
    locales = load_json(locales_filepath)

    target_dir = '/tmp/'
    s3 = S3()

    for locale in locales:

        filepath = '/v3/wildrift/{locale}/news.xml'.format(locale=locale['locale'])
        fullpath = target_dir + filepath

        collector = WildRiftNewsCollector(locale)
        items = collector.collect()

        selfLink = S3.generate_link(filepath)
        alternateLink = collector.construct_alternate_link() + 'news/'

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
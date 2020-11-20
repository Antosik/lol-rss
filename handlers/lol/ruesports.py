from sources.lol.ruesports import LOLRUeSportsCollector
from util.abstract.feed import Feed
from util.rss.generator import AtomGenerator
from util.s3 import S3


def handle(event={}, context={}):
    """Handler for AWS Lambda - LoL RU Esports"""

    target_dir = '/tmp/'
    filepath = '/v3/lol/ru/esports.xml'
    fullpath = target_dir + filepath

    s3 = S3()

    collector = LOLRUeSportsCollector()
    items = collector.collect()

    selfLink = S3.generate_link(filepath)
    alternateLink = collector.construct_alternate_link()

    feed = Feed()
    feed.generateUUID(selfLink)
    feed.setTitle('LoL Киберспорт [RU]')
    feed.setDescription('Статьи и новости с ru.lolesports.com')
    feed.setSelfLink(selfLink)
    feed.setAlternateLink(alternateLink)
    feed.setLanguage('ru-RU')
    feed.setItems(items)

    generator = AtomGenerator(feed)
    generator.generate(fullpath)

    s3.upload(fullpath, filepath[1:])

    return 'ok'

import requests
from typing import Dict, Any, List

from base import RssFeedCollector, RssFeedGenerator


class LOLeSportsCollector(RssFeedCollector):
    def get_items(self) -> List[Dict[str, any]]:
        response = requests.post(
            url='https://ru.lolesports.com/get-articles',
            json={'offset': 0, 'count': 10}
        )
        response.raise_for_status()
        return response.json()

    def filter_item(self, item: Dict[str, Any]) -> bool:
        return item['published']

    def transform_item(self: RssFeedCollector, item: Dict[str, Any]) -> Dict[str, Any]:
        result = {
            'id': str(item['id']),
            'title': item['title'],
            'link': {'href': 'https://ru.lolesports.com/articles/{0}'.format(item['id']), 'rel': 'alternate'},
            'author': {'name': item['nick_name']},
            'pubDate': item['published_at'],
            'updated': item['updated_at'],
        }

        if item['original']:
            result['enclosure'] = {'url': item['original'],
                                   'length': 0, 'type': 'image/jpg'}
        return result


def handle(event, context):
    collector = LOLeSportsCollector()

    generator = RssFeedGenerator(
        meta={
            'id': 'antosik:rulolesports',
            'title': 'LoL Киберспорт [RU]',
            'description': 'Статьи и новости с ru.lolesports.com',
            'link': {'href': 'https://ru.lolesports.com/articles', 'rel': 'alternate'},
            'author': {'name': 'Antosik', 'uri': 'https://github.com/Antosik'},
            'language': 'ru',
            'ttl': 15
        },
        collector=collector
    )

    filename = '/tmp/lolesports.xml'

    generator.generate(filename)
    generator.uploadToS3(filename)

    return 'ok'

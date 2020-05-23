from __future__ import absolute_import

import requests
from typing import Dict, Any, List

from util.rss.collector import RssFeedCollector
from util.rss.generator import RssFeedGenerator


class LOLeSportsCollector(RssFeedCollector):
    """Получение данных с ru.lolesports.com - киберспортивного портала о Лиге"""

    def get_items(self) -> List[Dict[str, any]]:
        """Получаем статьи с сайта"""
        response = requests.post(
            url='https://ru.lolesports.com/get-articles',
            json={'offset': 0, 'count': 10},
            headers={'user-agent': 'Antosik/lol-rss'}
        )
        response.raise_for_status()
        return response.json()

    def filter_item(self, item: Dict[str, Any]) -> bool:
        """Фильтруем неопубликованное"""
        return item['published']

    def transform_item(self: RssFeedCollector, item: Dict[str, Any]) -> Dict[str, Any]:
        """Приводим к виду, удобному для генератора RSS"""

        link = 'https://ru.lolesports.com/articles/{0}'.format(item['id'])
        uuid = RssFeedCollector.uuid_item(link)

        result = {
            'id': 'urn:uuid:{0}'.format(uuid),
            'title': item['title'].replace("\"", "\'"),
            'link': {'href': link, 'rel': 'alternate'},
            'author': {'name': item['nick_name']},
            'pubDate': item['published_at'],
            'updated': item['published_at'],
            'content': {'content': item['full_content'], 'type': 'html'}
        }

        if item['original']:
            result['enclosure'] = {'url': item['original'],
                                   'length': 0, 'type': 'image/jpg'}
        return result


def handle(event={}, context={}):
    """Обработчик для AWS Lambda"""

    collector = LOLeSportsCollector()

    target_dir = '/tmp/'

    dirpath = '/lol/'
    filename = 'esports.xml'
    filepath = dirpath + filename

    selflink = RssFeedGenerator.selflink_s3(filepath)
    generator = RssFeedGenerator(
        meta={
            'id': selflink,
            'title': 'LoL Киберспорт [RU]',
            'description': 'Статьи и новости с ru.lolesports.com',
            'link': [
                {
                    'href': selflink,
                    'rel': 'self'
                }, {
                    'href': 'https://ru.lolesports.com/articles',
                    'rel': 'alternate'
                }
            ],
            'author': {'name': 'Antosik', 'uri': 'https://github.com/Antosik'},
            'language': 'ru',
            'ttl': 15
        },
        collector=collector
    )

    generator.generate(target_dir + filepath)
    generator.uploadToS3(target_dir + filepath, filepath[1:])

    return 'ok'

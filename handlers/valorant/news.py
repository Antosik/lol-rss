from __future__ import absolute_import

import requests
from typing import Dict, Any, List

from util.rss.collector import RssFeedCollector
from util.rss.generator import RssFeedGenerator
from util.functions import normalize_url


class ValorantNewsCollector(RssFeedCollector):
    """Получение данных с официального сайта Valorant - beta.playvalorant.com/ru-ru/news"""

    def get_items(self) -> List[Dict[str, any]]:
        """Получаем новости с сайта"""
        response = requests.get(
            url='https://beta.playvalorant.com/page-data/ru-ru/news/page-data.json',
            headers={'user-agent': 'Antosik/lol-rss'}
        )
        response.raise_for_status()
        data = response.json()['result']['data']['allContentstackArticles']['nodes']

        return data[:30]

    def filter_item(self, item: Dict[str, Any]) -> bool:
        """Возвращаем все элементы - нет фильтра"""
        return True

    def transform_item(self: RssFeedCollector, item: Dict[str, Any]) -> Dict[str, Any]:
        """Приводим к виду, удобному для генератора RSS"""

        def transform_item_link(item: Dict[str, Any]) -> str:
            """Преобразование внутренней и внешней ссылки"""
            if item['external_link']:
                return item['external_link']
            else:
                return 'https://beta.playvalorant.com/ru-ru/{0}'.format(item['url']['url'])

        link = normalize_url(transform_item_link(item))
        uuid = RssFeedCollector.uuid_item(link)

        result = {
            'id': 'urn:uuid:{0}'.format(uuid),
            'title': item['title'].replace("\"", "\'"),
            'link': {'href': link, 'rel': 'alternate'},
            'pubDate': item['date'],
            'updated': item['date'],
            'content': {'content': item['description']}
        }

        if item['banner'] and item['banner']['url']:
            result['enclosure'] = {
                'url': item['banner']['url'],
                'length': 0,
                'type': 'image/jpg'
            }
        return result


def handle(event={}, context={}):
    """Обработчик для AWS Lambda"""

    collector = ValorantNewsCollector()

    target_dir = '/tmp/'

    dirpath = '/valorant/'
    filename = 'news.xml'
    filepath = dirpath + filename

    selflink = RssFeedGenerator.selflink_s3(filepath)
    generator = RssFeedGenerator(
        meta={
            'id': selflink,
            'title': 'Valorant Новости [RU]',
            'description': 'Последние новости',
            'link': [
                {
                    'href': selflink,
                    'rel': 'self'
                },
                {
                    'href': 'https://beta.playvalorant.com/ru-ru/news/',
                    'rel': 'alternate'
                }
            ],
            'author': {
                'name': 'Antosik',
                'uri': 'https://github.com/Antosik'
            },
            'language': 'ru',
            'ttl': 15
        },
        collector=collector
    )

    generator.generate(target_dir + filepath)
    generator.uploadToS3(target_dir + filepath, filepath[1:])

    return 'ok'

from __future__ import absolute_import

import requests
from typing import Dict, Any, List

from util.rss.collector import RssFeedCollector
from util.rss.generator import RssFeedGenerator
from util.functions import normalize_url


class LOLNewsCollector(RssFeedCollector):
    """Получение данных с официального сайта Лиги - ru.leagueoflegends.com/ru-ru/news"""

    def get_items(self) -> List[Dict[str, any]]:
        """Получаем новости с сайта"""
        response = requests.get(
            url='https://lolstatic-a.akamaihd.net/frontpage/apps/prod/harbinger-l10-website/ru-ru/production/ru-ru/page-data/latest-news/page-data.json',
            headers={'user-agent': 'Antosik/lol-rss'}
        )
        response.raise_for_status()
        data = response.json()

        def findNewsSection(sections):
            return next(section for section in sections if section['type'] == 'category_article_list_contentstack')

        data = response.json()['result']['pageContext']['data']['sections']
        return findNewsSection(data)['props']['articles'][:30]

    def filter_item(self, item: Dict[str, Any]) -> bool:
        """Возвращаем все элементы - нет фильтра"""
        return True

    def transform_item(self: RssFeedCollector, item: Dict[str, Any]) -> Dict[str, Any]:
        """Приводим к виду, удобному для генератора RSS"""

        def transform_item_link(link: Dict[str, str]) -> str:
            """Преобразование внутренней и внешней ссылки"""
            if link['internal']:
                return 'https://ru.leagueoflegends.com/ru-ru/{0}'.format(link['url'])
            else:
                return link['url']

        link = normalize_url(transform_item_link(item['link']))
        uuid = RssFeedCollector.uuid_item(link)
        author = {'name': ', '.join(item['authors'])}
        category = {
            'term': 'category',
            'label': item['category']
        }

        result = {
            'id': 'urn:uuid:{0}'.format(uuid),
            'title': item['title'].replace("\"", "\'"),
            'link': {'href': link, 'rel': 'alternate'},
            'author': author,
            'pubDate': item['date'],
            'updated': item['date'],
            'category': category
        }

        if item['imageUrl']:
            result['enclosure'] = {
                'url': item['imageUrl'],
                'length': 0,
                'type': 'image/jpg'
            }
        return result


def handle(event={}, context={}):
    """Обработчик для AWS Lambda"""

    collector = LOLNewsCollector()

    target_dir = '/tmp/'

    dirpath = '/lol/'
    filename = 'news.xml'
    filepath = dirpath + filename

    selflink = RssFeedGenerator.selflink_s3(filepath)
    generator = RssFeedGenerator(
        meta={
            'id': selflink,
            'title': 'LoL Новости [RU]',
            'description': 'Новости и обновления игры',
            'link': [
                {
                    'href': selflink,
                    'rel': 'self'
                },
                {
                    'href': 'https://ru.leagueoflegends.com/ru-ru/news/',
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

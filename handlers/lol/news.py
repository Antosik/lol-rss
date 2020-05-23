from __future__ import absolute_import

import json
import os
import requests
from typing import Dict, Any, List

from util.rss.collector import RssFeedCollector
from util.rss.generator import RssFeedGenerator
from util.functions import normalize_url


def construct_alternate_link(region: str, locale: str):
    """Construct link to League of Legends site for the specific locale and region"""

    return 'https://{region}.leagueoflegends.com/{locale}/'.format(
        region=region,
        locale=locale.lower()
    )


class LOLNewsCollector(RssFeedCollector):
    """Получение данных с официального сайта Лиги - ru.leagueoflegends.com/ru-ru/news"""

    def __init__(self, server: Dict[str, str]):
        """Конструктор класса

        Arguments:
            server {Dict[str, str]} -- Server information
        """
        self._server = server

    def get_items(self) -> List[Dict[str, any]]:
        """Получаем новости с сайта"""

        url = 'https://lolstatic-a.akamaihd.net/frontpage/apps/prod/harbinger-l10-website/{locale}/production/{locale}/page-data/latest-news/page-data.json'.format(
            locale=self._server['language'].lower()
        )
        response = requests.get(
            url=url,
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
                return construct_alternate_link(region=self._server['region'], locale=self._server['language']) + '/' + link['url']
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

    target_dir = '/tmp/'
    servers_filepath = os.path.join(os.path.dirname(__file__), './data/news.json')

    with open(servers_filepath) as json_file:

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
                            'href': construct_alternate_link(region=server['region'], locale=server['language']),
                            'rel': 'alternate'
                        }
                    ],
                    'author': {'name': 'Antosik', 'uri': 'https://github.com/Antosik'},
                    'language': server['language'],
                    'ttl': 15
                },
                collector=collector
            )

            generator.generate(target_dir + filepath)
            generator.uploadToS3(target_dir + filepath, filepath[1:])

    return 'ok'

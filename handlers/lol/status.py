from __future__ import absolute_import

import json
import os
import requests
from typing import Dict, Any, List

from util.rss.collector import RssFeedCollector
from util.rss.generator import RssFeedGenerator


def construct_alternate_link(region: str, locale: str):
    """Construct link to Server status page for the specific locale and region"""

    return 'https://status.riotgames.com/?region={region}&locale={locale}&product=leagueoflegends'.format(
        region=region,
        locale=locale
    )


class LOLServerStatusCollector(RssFeedCollector):
    """Получение данных о статусе сервера"""

    def __init__(self, server: Dict[str, str]):
        """Конструктор класса

        Arguments:
            server {Dict[str, str]} -- Server information
        """
        self._server = server

    def get_items(self) -> List[Dict[str, any]]:
        """Получаем статусы с сайта"""
        response = requests.get(
            url='https://lol.secure.dyn.riotcdn.net/channels/public/x/status/{id}.json'.format(id=self._server['id']),
            headers={'user-agent': 'Antosik/lol-rss'}
        )
        response.raise_for_status()
        json = response.json()

        def expandCategory(category):
            results = []

            for entry in category:
                title = self.take_locale(entry['titles'])["content"]

                for update in entry['updates']:
                    results.append({'title': title, **update})

            return results

        return expandCategory(json['maintenances']) + expandCategory(json['incidents'])

    def filter_item(self, item: Dict[str, Any]) -> bool:
        """Фильтруем неопубликованное"""
        return item['publish']

    def transform_item(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """Приводим к виду, удобному для генератора RSS"""

        link = construct_alternate_link(region=self._server['region'], locale=self._server['locale'])
        uuid = RssFeedCollector.uuid_item(link + '&id={0}'.format(item['id']))
        return {
            'id': 'urn:uuid:{0}'.format(uuid),
            'title': item['title'].replace("\"", "\'"),
            'description': self.take_locale(item['translations'])["content"].replace("\"", "\'"),
            'link': {
                'href': link,
                'rel': 'alternate'
            },
            'author': {'name': item['author']},
            'pubDate': item['created_at'],
            'updated': item['created_at'],
        }

    def take_locale(self, items):
        """Нужен для получения названия и описания на русском языке"""
        return next(item for item in items if item['locale'] == self._server['locale'])


def handle(event={}, context={}):
    """Обработчик для AWS Lambda"""

    target_dir = '/tmp/'
    servers_filepath = os.path.join(os.path.dirname(__file__), './data/status.json')

    with open(servers_filepath) as json_file:

        servers = json.load(json_file)

        for server in servers:

            collector = LOLServerStatusCollector(server)

            dirpath = '/lol/{region}/'.format(region=server['region'])
            filename = 'status.xml'
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
                            'href': construct_alternate_link(region=server['region'], locale=server['locale']),
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

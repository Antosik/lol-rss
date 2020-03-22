import requests
from typing import Dict, Any, List

from base import RssFeedCollector, RssFeedGenerator


class LOLServerStatusCollector(RssFeedCollector):
    def get_items(self) -> List[Dict[str, any]]:
        """Получаем статусы с сайта"""
        response = requests.get(
            url='https://lol.secure.dyn.riotcdn.net/channels/public/x/status/ru1.json',
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
        uuid = RssFeedCollector.uuid_item('https://status.riotgames.com/?region=ru&locale=ru_RU&product=leagueoflegends&id={0}'.format(item['id']))
        return {
            'id': 'urn:uuid:{0}'.format(uuid),
            'title': item['title'].replace("\"", "\'"),
            'description': self.take_locale(item['translations'])["content"].replace("\"", "\'"),
            'link': {
                'href': 'https://status.riotgames.com/?region=ru&locale=ru_RU&product=leagueoflegends',
                'rel': 'alternate'
            },
            'author': {'name': item['author']},
            'pubDate': item['created_at'],
            'updated': item['updated_at'],
        }

    def take_locale(self, items):
        """Нужен для получения названия и описания на русском языке"""
        return next(item for item in items if item['locale'] == 'ru_RU')


def handle(event={}, context={}):
    """Обработчик для AWS Lambda"""
    collector = LOLServerStatusCollector()

    filename = 'lolstatus.xml'
    filepath = '/tmp/' + filename
    selflink = RssFeedGenerator.selflink_s3(filename)

    generator = RssFeedGenerator(
        meta={
            'id': selflink,
            'title': 'LoL Статус сервера [RU]',
            'description': 'Статус сервера: Тех.обслуживание, ошибки и многое другое',
            'link': [
                {
                    'href': selflink,
                    'rel': 'self'
                },
                {
                    'href': 'https://status.riotgames.com/?region=ru&locale=ru_RU&product=leagueoflegends',
                    'rel': 'alternate'
                }
            ],
            'author': {'name': 'Antosik', 'uri': 'https://github.com/Antosik'},
            'language': 'ru',
            'ttl': 15
        },
        collector=collector
    )

    generator.generate(filepath)
    generator.uploadToS3(filepath, filename)

    return 'ok'

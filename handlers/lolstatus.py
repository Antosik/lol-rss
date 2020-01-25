import json
import requests
from typing import Dict, Any, List

from base import RssFeedCollector, RssFeedGenerator


class LOLServerStatusCollector(RssFeedCollector):
    def get_items(self) -> List[Dict[str, any]]:
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
        return item['publish'] == True

    def transform_item(self, item: Dict[str, Any]) -> Dict[str, Any]:
        return {
            'id': str(item['id']),
            'title': item['title'],
            'description': self.take_locale(item['translations'])["content"],
            'link': {'href': 'https://status.riotgames.com/?region=ru&locale=ru_RU&product=leagueoflegends', 'rel': 'alternate'},
            'author': {'name': item['author']},
            'pubDate': item['created_at'],
            'updated': item['updated_at'],
        }

    def take_locale(self, items):
        return next(item for item in items if item['locale'] == 'ru_RU')


def handle(event, context):
    collector = LOLServerStatusCollector()

    generator = RssFeedGenerator(
        meta={
            'id': 'antosik:rulolstatus',
            'title': 'LoL Статус сервера [RU]',
            'description': 'Статус сервера: Тех.обслуживание, ошибки и многое другое',
            'link': {'href': 'https://status.riotgames.com/?region=ru&locale=ru_RU&product=leagueoflegends', 'rel': 'alternate'},
            'author': {'name': 'Antosik', 'uri': 'https://github.com/Antosik'},
            'language': 'ru',
            'ttl': 15
        },
        collector=collector
    )

    filename = '/tmp/lolstatus.xml'

    generator.generate(filename)
    generator.uploadToS3(filename)

    return 'ok'

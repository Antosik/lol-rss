import requests
from typing import Dict, Any, List

from util.rss.collector import RssFeedCollector


class RiotServerStatusCollector(RssFeedCollector):
    """Получение данных о статусе сервера"""

    def __init__(self, product: str, source_url: str, server: Dict[str, str]):
        """Конструктор класса

        Arguments:
            product {str} -- Product name
            source_url {Dict[str, str]} -- Data source url
            server {Dict[str, str]} -- Server information
        """
        self._product = product
        self._source_url = source_url
        self._server = server

    def get_items(self) -> List[Dict[str, any]]:
        """Получаем статусы с сайта"""
        response = requests.get(
            url='{source_url}/{id}.json'.format(source_url=self._source_url, id=self._server['id']),
            headers={'user-agent': 'Antosik/lol-rss'}
        )
        response.raise_for_status()
        json = response.json()

        def expandCategory(category):
            results = []

            for entry in category:
                locale_title = self.take_locale(entry['titles'])["content"]
                title = self.take_locale(entry['titles'], "en-US")["content"] if not locale_title else locale_title

                for update in entry['updates']:
                    results.append({'title': title, **update})

            return results

        return expandCategory(json['maintenances']) + expandCategory(json['incidents'])

    def filter_item(self, item: Dict[str, Any]) -> bool:
        """Фильтруем неопубликованное"""
        return item['publish']

    def construct_alternate_link(self):
        """Construct link to Server status page for the specific locale and region"""

        return 'https://status.riotgames.com/?region={region}&locale={locale}&product={product}'.format(
            region=self._server['locale'],
            locale=self._server['locale'].replace('-', '_'),
            product=self._product
        )

    def transform_item(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """Приводим к виду, удобному для генератора RSS"""

        link = self.construct_alternate_link()
        uuid = RssFeedCollector.uuid_item(link + '&id={0}'.format(item['id']))

        locale_description = self.take_locale(item['translations'])["content"]
        description = self.take_locale(item['translations'], "en-US")["content"] if not locale_description else locale_description

        return {
            'id': 'urn:uuid:{0}'.format(uuid),
            'title': item['title'].replace("\"", "\'"),
            'link': {'href': link, 'rel': 'alternate'},
            'author': {'name': item['author']},
            'pubDate': item['created_at'],
            'updated': item['created_at'],
            'description': description.replace("\"", "\'"),
        }

    def take_locale(self, items, locale=None):
        """Нужен для получения названия и описания на русском языке"""
        if locale is None:
            locale = self._server['locale']
        return next(item for item in items if item['locale'] == locale.replace('-', '_'))

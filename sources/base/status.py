import requests
from typing import Any, Dict, List, Optional

from util.rss.collector import RssFeedCollector


class RiotServerStatusCollector(RssFeedCollector):
    """The class that responsible for collecting server status from https://status.riotgames.com/"""

    def __init__(self, product: str, source_url: str, server: Dict[str, str]):
        """Constructor

        Arguments:
            product {str} -- Product name
            source_url {str} -- Data source url
            server {Dict[str, str]} -- Server information
        """
        self._product = product
        self._source_url = source_url
        self._server = server

    def get_items(self) -> List[Dict[str, Any]]:
        """Get server status information"""
        response = requests.get(
            url='{source_url}/{id}.json'.format(source_url=self._source_url, id=self._server['id']),
            headers={'user-agent': 'Antosik/lol-rss'}
        )
        response.raise_for_status()
        json = response.json()

        def expandCategory(category: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
            results = []

            for entry in category:
                locale_title = self.take_locale(entry['titles'])
                title = self.take_locale(entry['titles'], "en-US") if not locale_title else locale_title

                for update in entry['updates']:
                    results.append({'title': title, **update})

            return results

        return expandCategory(json['maintenances']) + expandCategory(json['incidents'])

    def filter_item(self, item: Dict[str, Any]) -> bool:
        """Filter unpublished content"""
        return item['publish']

    def construct_alternate_link(self) -> str:
        """Construct link to Server status page for the specific locale and region"""

        return 'https://status.riotgames.com/?region={region}&locale={locale}&product={product}'.format(
            region=self._server['locale'],
            locale=self._server['locale'].replace('-', '_'),
            product=self._product
        )

    def transform_item(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """Transform entries to RSS format"""

        link = self.construct_alternate_link()
        uuid = RssFeedCollector.uuid_item(link + '&id={0}'.format(item['id']))

        description = self.take_locale(item['translations']) or self.take_locale(item['translations'], "en-US") or ""

        return {
            'id': 'urn:uuid:{0}'.format(uuid),
            'title': item['title'].replace("\"", "\'"),
            'link': {'href': link, 'rel': 'alternate'},
            'author': {'name': item['author']},
            'pubDate': item['created_at'],
            'updated': item['created_at'],
            'description': description.replace("\"", "\'"),
        }

    def take_locale(self, items: List[Dict[str, Any]], locale: str = None) -> Optional[str]:
        """Get translation for the locale"""
        if locale is None:
            locale = self._server['locale']

        result = next((item for item in items if item['locale'] == locale.replace('-', '_')), None)

        return None if (result is None or "content" not in result) else result["content"]

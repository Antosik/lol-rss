import requests
from typing import Dict, Any, List

from util.rss.collector import RssFeedCollector
from util.functions import normalize_url


class ValorantNewsCollector(RssFeedCollector):
    """The class that responsible for collecting news from https://playvalorant.com"""

    @staticmethod
    def construct_alternate_link(locale: str) -> str:
        """Construct link to Valorant site for the specific locale and region"""

        return 'https://playvalorant.com/{locale}/'.format(
            locale=locale.lower()
        )

    def __init__(self, locale: Dict[str, str]):
        """Constructor

        Arguments:
            locale {Dict[str, str]} -- Locale information
        """
        self._locale = locale

    def get_items(self) -> List[Dict[str, any]]:
        """Get news from website"""
        response = requests.get(
            url='https://playvalorant.com/page-data/{locale}/news/page-data.json'.format(
                locale=self._locale['locale'].lower()
            ),
            headers={'user-agent': 'Antosik/lol-rss'}
        )
        response.raise_for_status()
        data = response.json()['result']['data']['allContentstackArticles']['nodes']

        return data[:30]

    def filter_item(self, item: Dict[str, Any]) -> bool:
        """No filter - return all items"""
        return True

    def transform_item(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """Transform entries to RSS format"""

        def transform_item_link(item: Dict[str, Any]) -> str:
            """Transformation of internal/external link"""
            if item['external_link']:
                return item['external_link']
            else:
                return ValorantNewsCollector.construct_alternate_link(
                    locale=self._locale['locale']
                ) + '/' + item['url']['url']

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

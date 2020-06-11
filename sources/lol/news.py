import requests
from typing import Any, Dict, List

from util.rss.collector import RssFeedCollector
from util.functions import normalize_url


class LOLNewsCollector(RssFeedCollector):
    """The class that responsible for collecting news from https://leagueoflegends.com"""

    @staticmethod
    def construct_alternate_link(region: str, locale: str) -> str:
        """Construct link to League of Legends site for the specific locale and region"""

        return 'https://{region}.leagueoflegends.com/{locale}/'.format(
            region=region,
            locale=locale.lower()
        )

    def __init__(self, server: Dict[str, str]):
        """Constructor

        Arguments:
            server {Dict[str, str]} -- Server information
        """
        self._server = server

    def get_items(self) -> List[Dict[str, Any]]:
        """Get news from website"""

        url = 'https://lolstatic-a.akamaihd.net/frontpage/apps/prod/harbinger-l10-website/{locale}/production/{locale}/page-data/latest-news/page-data.json'.format(
            locale=self._server['locale'].lower()
        )
        response = requests.get(
            url=url,
            headers={'user-agent': 'Antosik/lol-rss'}
        )
        response.raise_for_status()
        data = response.json()

        def findNewsSection(sections: List[Dict[str, Any]]) -> Dict[str, Any]:
            return next(section for section in sections if section['type'] == 'category_article_list_contentstack')

        data = response.json()['result']['pageContext']['data']['sections']
        return findNewsSection(data)['props']['articles'][:30]

    def filter_item(self, item: Dict[str, Any]) -> bool:
        """No filter - return all items"""
        return True

    def transform_item(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """Transform entries to RSS format"""

        def transform_item_link(link: Dict[str, str]) -> str:
            """Transformation of internal/external link"""
            if link['internal']:
                return LOLNewsCollector.construct_alternate_link(
                    region=self._server['region'],
                    locale=self._server['locale']
                ) + '/' + link['url']
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
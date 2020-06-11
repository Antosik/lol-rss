import requests
from typing import Any, Dict, List

from util.rss.collector import RssFeedCollector


class LOLRUeSportsCollector(RssFeedCollector):
    """The class that responsible for collecting esports news from https://ru.lolesports.com"""

    def get_items(self) -> List[Dict[str, Any]]:
        """Get news from website"""
        response = requests.post(
            url='https://ru.lolesports.com/get-articles',
            json={'offset': 0, 'count': 10},
            headers={'user-agent': 'Antosik/lol-rss'}
        )
        response.raise_for_status()
        return response.json()

    def filter_item(self, item: Dict[str, Any]) -> bool:
        """Filter unpublished content"""
        return item['published']

    def transform_item(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """Transform entries to RSS format"""

        link = 'https://ru.lolesports.com/articles/{0}'.format(item['id'])
        uuid = RssFeedCollector.uuid_item(link)

        result = {
            'id': 'urn:uuid:{0}'.format(uuid),
            'title': item['title'].replace("\"", "\'"),
            'link': {'href': link, 'rel': 'alternate'},
            'author': {'name': item['nick_name']},
            'pubDate': item['published_at'],
            'updated': item['published_at'],
            'content': {'content': item['full_content'], 'type': 'html'}
        }

        if item['original']:
            result['enclosure'] = {'url': item['original'],
                                   'length': 0, 'type': 'image/jpg'}

        return result

import requests
from typing import Any, Dict, Final, List

from util.abstract.collector import DataCollector
from util.abstract.item import FeedItem


class LOLRUeSportsCollector(DataCollector):
    """The class that responsible for collecting esports news from https://ru.lolesports.com"""

    ARTICLES_COUNT_TO_FETCH: Final = 10

    # region Data Collection
    def get_items(self) -> List[Dict[str, Any]]:
        response = requests.post(
            url='https://ru.lolesports.com/get-articles',
            json={'offset': 0, 'count': self.ARTICLES_COUNT_TO_FETCH},
            headers={'user-agent': 'Antosik/lol-rss'}
        )
        response.raise_for_status()
        return response.json()

    def filter_item(self, item: Dict[str, Any]) -> bool:
        return item['published']

    def transform_item(self, item: Dict[str, Any]) -> FeedItem:
        link = self.construct_alternate_link() + '/' + str(item['id'])

        result = FeedItem()
        result.generateUUID(link)
        result.setTitle(item['title'])
        result.setLink(link)
        result.setAuthor(item['nick_name'])
        result.setCreatedAt(item['published_at'])
        result.setUpdatedAt(item['published_at'])

        if item['original']:
            result.setImage(item['original'])

        return result
    # endregion Data Collection

    # region Helpers
    def construct_alternate_link(self) -> str:
        return 'https://ru.lolesports.com/articles/'
    # endregion Helpers

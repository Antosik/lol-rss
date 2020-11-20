from typing import Any, Dict, Final, List

from util.abstract.collector import DataCollector
from util.abstract.item import FeedItem


class ValorantNewsCollector(DataCollector):
    """The class that responsible for collecting news from https://playvalorant.com"""

    ARTICLES_COUNT_TO_FETCH: Final = 30

    def __init__(self, locale: Dict[str, str]):
        """Constructor

        Arguments:
            locale {Dict[str, str]} -- Locale information
        """
        self.__locale = locale

    # region Data Collection
    def get_data(self) -> Any:
        return self._request(
            'https://playvalorant.com/page-data/{locale}/news/page-data.json'.format(
                locale=self.__locale['locale'].lower()
            )
        )

    def get_items(self) -> List[Dict[str, Any]]:
        raw = self.get_data()
        data = raw['result']['data']['allContentstackArticles']['nodes']
        return data[:self.ARTICLES_COUNT_TO_FETCH]

    def filter_item(self, item: Dict[str, Any]) -> bool:
        return True

    def transform_item(self, item: Dict[str, Any]) -> FeedItem:

        link = self.__transform_item_link(item)

        result = FeedItem()
        result.generateUUID(link)
        result.setTitle(item['title'])
        result.setSummary(item['description'])
        result.setLink(link)
        result.setCreatedAt(item['date'])
        result.setUpdatedAt(item['date'])

        if item['banner'] and item['banner']['url']:
            result.setImage(item['banner']['url'])

        return result
    # endregion Data Collection

    # region Helpers
    def construct_alternate_link(self) -> str:
        return 'https://playvalorant.com/{locale}/'.format(
            locale=self.__locale['locale'].lower()
        )

    def __transform_item_link(self, item: Dict[str, Any]) -> str:
        """Transformation of internal/external link"""
        if item['external_link']:
            return item['external_link']
        else:
            return self.construct_alternate_link() + '/' + item['url']['url']
    # endregion Helpers

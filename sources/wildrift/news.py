from typing import Any, Dict, Final, List, Optional

from datetime import datetime, timezone

from util.abstract.collector import DataCollector
from util.abstract.item import FeedItem


class WildRiftNewsCollector(DataCollector):
    """The class that responsible for collecting news from https://wildrift.leagueoflegends.com/"""

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
            'https://wildrift.leagueoflegends.com/page-data/{locale}/news/page-data.json'.format(
                locale=self.__locale['locale'].lower()
            )
        )

    def get_items(self) -> List[Dict[str, Any]]:
        raw = self.get_data()
        data = raw['result']['data']['allContentstackArticles']['articles']
        return data[:self.ARTICLES_COUNT_TO_FETCH]

    def filter_item(self, item: Dict[str, Any]) -> bool:
        return True

    def transform_item(self, item: Dict[str, Any]) -> FeedItem:

        link = self.__transform_item_link(item)
        date = datetime.strptime(item['date'], "%m-%d-%Y").replace(tzinfo=timezone.utc)

        result = FeedItem()
        result.generateUUID(link)
        result.setTitle(item['title'])
        result.setSummary(item['description'])
        result.setLink(link)
        result.setCreatedAt(date)
        result.setUpdatedAt(date)

        image = self.__getItemBannerImage(item)
        if image:
            result.setImage(image)

        category = self.__getItemCategory(item)
        if category:
            result.setCategory(category)

        return result
    # endregion Data Collection

    # region Helpers
    def construct_alternate_link(self) -> str:
        return 'https://wildrift.leagueoflegends.com/{locale}/'.format(
            locale=self.__locale['locale'].lower()
        )

    def __getItemBannerImage(self, item: Dict[str, Any]) -> Optional[str]:
        if item['featuredImage'] and item['featuredImage']['banner'] and item['featuredImage']['banner']['url']:
            return item['featuredImage']['banner']['url']
        return None

    def __getItemCategory(self, item: Dict[str, Any]) -> Optional[str]:
        if item['categories'] and len(item['categories']) > 0 and item['categories'][0]['title']:
            return item['categories'][0]['title']
        return None

    def __transform_item_link(self, item: Dict[str, Any]) -> str:
        """Transformation of internal/external link"""
        if item['youtubeLink']:
            return item['youtubeLink']
        elif item['externalLink']:
            return item['externalLink']
        else:
            return self.construct_alternate_link() + '/' + item['link']['url']
    # endregion Helpers

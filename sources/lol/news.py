from typing import Any, Dict, List, Final

from util.abstract.collector import DataCollector
from util.abstract.item import FeedItem


class LOLNewsCollector(DataCollector):

    ARTICLES_COUNT_TO_FETCH: Final = 30

    def __init__(self, server: Dict[str, str]):
        """Constructor

        Args:
            server (Dict[str, str]): Server information
        """
        self.__server = server

    # region Data Collection
    def get_data(self) -> Any:
        return self._request(
            'https://lolstatic-a.akamaihd.net/frontpage/apps/prod/harbinger-l10-website/{locale}/production/{locale}/page-data/latest-news/page-data.json'.format(
                locale=self.__server['locale'].lower()
            )
        )

    def get_items(self) -> List[Dict[str, Any]]:
        raw = self.get_data()
        data = raw['result']['pageContext']['data']['sections']
        return self.__findNewsSection(data)['props']['articles'][:self.ARTICLES_COUNT_TO_FETCH]

    def filter_item(self, item: Dict[str, Any]) -> bool:
        return True

    def transform_item(self, item: Dict[str, Any]) -> FeedItem:

        link = self.__transform_item_link(item['link'])

        result = FeedItem()
        result.generateUUID(link)
        result.setTitle(item['title'])
        result.setLink(link)
        result.setAuthor(item['authors'])
        result.setCreatedAt(item['date'])
        result.setUpdatedAt(item['date'])
        result.setCategory(item['category'])

        if item['imageUrl']:
            result.setImage(item['imageUrl'])

        return result
    # endregion Data Collection

    # region Helpers
    def construct_alternate_link(self) -> str:
        return 'https://{region}.leagueoflegends.com/{locale}/'.format(
            region=self.__server['region'],
            locale=self.__server['locale'].lower()
        )

    def __findNewsSection(self, sections: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Search for a section with news articles

        Args:
            sections (List[Dict[str, Any]]): Array of raw sections

        Returns:
            Dict[str, Any]: Section with news articles
        """
        return next(section for section in sections if section['type'] == 'category_article_list_contentstack')

    def __transform_item_link(self, link: Dict[str, str]) -> str:
        """Transformation of internal/external link

        Args:
            link (Dict[str, str]): Link object

        Returns:
            str: Normalized link
        """
        if link['internal']:
            return self.construct_alternate_link() + '/' + link['url']
        else:
            return link['url']
    # endregion Helpers

from typing import Any, Dict, List, Optional

from util.abstract.collector import DataCollector
from util.abstract.item import FeedItem


class ServerStatusCollector(DataCollector):
    """The class that responsible for collecting server status from https://status.riotgames.com/"""

    def __init__(self, server: Dict[str, str]):
        """Constructor

        Arguments:
            server {Dict[str, str]} -- Server information
        """
        self.__server = server

    def get_server(self) -> Dict[str, str]:
        return self.__server

    # region Items Processing
    def get_items(self) -> List[Dict[str, Any]]:
        """Get server status information"""

        json = self.get_data()

        return self.__expandCategory(json['maintenances']) + self.__expandCategory(json['incidents'])

    def filter_item(self, item: Dict[str, Any]) -> bool:
        """Filter unpublished content"""
        return item['publish']

    def transform_item(self, item: Dict[str, Any]) -> FeedItem:
        """Transform entries to RSS format"""

        link = self.construct_alternate_link() + "&id=" + str(item['id'])
        summary = self.__take_locale(item['translations']) or self.__take_locale(item['translations'], "en-US") or ""

        result = FeedItem()
        result.generateUUID(link)
        result.setTitle(item['title'])
        result.setSummary(summary)
        result.setLink(link)
        result.setAuthor(item['author'])
        result.setCreatedAt(item['created_at'])
        result.setUpdatedAt(item['created_at'])
        return result
    # endregion Items Processing

    # region Helpers
    def __take_locale(self, items: List[Dict[str, Any]], locale: str = None) -> Optional[str]:
        """Get translation for the locale"""
        if locale is None:
            locale = self.__server['locale']

        result = next((item for item in items if item['locale'] == locale.replace('-', '_')), None)

        return None if (result is None or "content" not in result) else result["content"]

    def __expandCategory(self, category: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        results = []

        for entry in category:
            locale_title = self.__take_locale(entry['titles'])
            title = self.__take_locale(entry['titles'], "en-US") if not locale_title else locale_title

            for update in entry['updates']:
                results.append({'title': title, **update})

        return results
    # endregion Helpers

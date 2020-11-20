from typing import Any, Dict, List, Union

import requests

from .item import FeedItem


class DataCollector(object):
    """Base class for receiving, converting and transforming data into usable for RSS"""

    # region Utils
    def _request(self, url: str) -> Union[List[Dict[str, Any]], Dict[str, Any]]:
        response = requests.get(
            url=url,
            headers={'user-agent': 'Antosik/lol-rss'}
        )
        response.raise_for_status()
        return response.json()

    def construct_alternate_link(self) -> str:
        """Construct link to news page

        Raises:
            NotImplementedError: Since this is an abstract method - there is no implementation - throw an exception

        Returns:
            str -- link to news page
        """
        raise NotImplementedError
    # endregion Utils

    # region Data Collection
    def get_data(self) -> Any:
        """Abstract method for obtaining raw data

        Raises:
            NotImplementedError: Since this is an abstract method - there is no implementation - throw an exception

        Returns:
            Any -- Raw data
        """
        raise NotImplementedError

    def get_items(self) -> List[Dict[str, Any]]:
        """Abstract method for obtaining raw items

        Raises:
            NotImplementedError: Since this is an abstract method - there is no implementation - throw an exception

        Returns:
            JSONArray -- List of items
        """
        raise NotImplementedError

    def filter_item(self, item: Dict[str, Any]) -> bool:
        """Abstract method for filtering elements

        Arguments:
            item {JSONTree} -- Item to filter

        Raises:
            NotImplementedError: Since this is an abstract method - there is no implementation - throw an exception

        Returns:
            bool -- Leave the item in the list (True) or remove (False)
        """
        raise NotImplementedError

    def transform_item(self, item: Dict[str, Any]) -> FeedItem:
        """Abstract method for transforming elements into usable for RSS / Atom

        Arguments:
            item {JSONTree} -- Item to transform

        Raises:
            NotImplementedError: Since this is an abstract method - there is no implementation - throw an exception

        Returns:
            FeedItem -- Transformed item
        """

        raise NotImplementedError

    def collect(self) -> List[FeedItem]:
        """Method that causes the receipt, filtering and subsequent transformation of elements

        Returns:
            List[FeedItem] -- List of items suitable for RSS / Atom
        """
        items = self.get_items()

        results: List[FeedItem] = []

        for item in items:
            if self.filter_item(item):
                transformed = self.transform_item(item)
                if isinstance(transformed, list):
                    results.extend(transformed)
                else:
                    results.append(transformed)

        results.sort()

        return results
    # endregion Data Collection

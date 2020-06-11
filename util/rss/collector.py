import uuid
from typing import Dict, Any, List


class RssFeedCollector(object):
    """Base class for receiving, converting and transforming data into usable for RSS"""

    @staticmethod
    def uuid_item(url: str) -> uuid.UUID:
        """Generate a unique ID for each item

        Arguments:
            url {str} -- URL for the item

        Returns:
            str -- Generated ID
        """
        return uuid.uuid5(uuid.NAMESPACE_URL, url)

    def get_items(self) -> List[Dict[str, Any]]:
        """Abstract method for obtaining data

        Raises:
            NotImplementedError: Since this is an abstract method - there is no implementation - throw an exception

        Returns:
            List[Dict[str, Any]] -- List of items
        """
        raise NotImplementedError

    def filter_item(self, item: Dict[str, Any]) -> bool:
        """Abstract method for filtering elements

        Arguments:
            item {Dict[str, Any]} -- Item to filter

        Raises:
            NotImplementedError: Since this is an abstract method - there is no implementation - throw an exception

        Returns:
            bool -- Leave the item in the list (True) or remove (False)
        """
        raise NotImplementedError

    def transform_item(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """Abstract method for transforming elements into usable for RSS / Atom

        Arguments:
            item {Dict[str, Any]} -- Item to transform

        Raises:
            NotImplementedError: Since this is an abstract method - there is no implementation - throw an exception

        Returns:
            Dict[str, Any] -- Transformed item
        """

        raise NotImplementedError

    def collect(self) -> List[Dict[str, Any]]:
        """Method that causes the receipt, filtering and subsequent transformation of elements

        Returns:
            List[Dict[str, Any]] -- List of items suitable for RSS / Atom
        """
        items = self.get_items()
        results = []

        for item in items:
            if self.filter_item(item):
                transformed = self.transform_item(item)
                if isinstance(transformed, list):
                    results.extend(transformed)
                else:
                    results.append(transformed)

        results.sort(key=(lambda x: x['pubDate']))

        return results

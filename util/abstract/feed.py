from typing import Any, Dict, Final, List, Optional

from os import environ as env
from uuid import uuid5, NAMESPACE_URL

from .item import FeedItem
from ..functions.normalize_url import normalize_url


class Feed(object):
    """Feed representation"""

    TTL: Final = env.get('TTL') or 10
    AuthorName: Final = 'Antosik'
    AuthorUri: Final = 'https://github.com/Antosik'

    def __init__(self):
        self.__id = None
        self.__title = None
        self.__description = None
        self.__selfLink = None
        self.__alternateLink = None
        self.__language = None
        self.__authorName = Feed.AuthorName
        self.__authorUri = Feed.AuthorUri
        self.__ttl = Feed.TTL
        self.__items = []

    # region Getters & Setters
    def getId(self) -> Optional[str]:
        return self.__id

    def setId(self, id: str) -> 'Feed':
        self.__id = id
        return self

    def generateUUID(self, url: str) -> 'Feed':
        return self.setId('urn:uuid:{0}'.format(uuid5(NAMESPACE_URL, normalize_url(url))))

    def getTitle(self) -> Optional[str]:
        return self.__title

    def setTitle(self, title: str) -> 'Feed':
        self.__title = title
        return self

    def getDescription(self) -> Optional[str]:
        return self.__description

    def setDescription(self, description: str) -> 'Feed':
        self.__description = description
        return self

    def getSelfLink(self) -> Optional[str]:
        return self.__selfLink

    def setSelfLink(self, selfLink: str) -> 'Feed':
        self.__selfLink = selfLink
        return self

    def getAlternateLink(self) -> Optional[str]:
        return self.__alternateLink

    def setAlternateLink(self, alternateLink: str) -> 'Feed':
        self.__alternateLink = alternateLink
        return self

    def getLanguage(self) -> Optional[str]:
        return self.__language

    def setLanguage(self, language: str) -> 'Feed':
        self.__language = language
        return self

    def getAuthorName(self) -> str:
        return self.__authorName

    def setAuthorName(self, authorName: str) -> 'Feed':
        self.__authorName = authorName
        return self

    def getAuthorUri(self) -> str:
        return self.__authorUri

    def setAuthorUri(self, authorUri: str) -> 'Feed':
        self.__authorUri = authorUri
        return self

    def getTTL(self) -> int:
        return self.__ttl

    def getItems(self) -> List[FeedItem]:
        return self.__items

    def setItems(self, items: List[FeedItem]) -> 'Feed':
        self.__items = items
        self.__items.sort()
        return self
    # endregion Getters & Setters

    # region Overrides
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Feed):
            return False
        return set(self.getItems()) == set(other.getItems())

    def __hash__(self):
        return hash(self.getId())

    def __repr__(self):
        return str(self.toDict())
    # endregion Overrides

    # region Utils
    def toDict(self) -> Dict[str, Any]:
        """Convert Feed to Dict

        Returns:
            Dict[str, Any]: Dict representation
        """
        return {
            'id': self.__id,
            'title': self.__title,
            'description': self.__description,
            'selfLink': self.__selfLink,
            'alternateLink': self.__alternateLink,
            'language': self.__language,
            'authorName': self.__authorName,
            'authorUri': self.__authorUri,
            'ttl': self.__ttl,
            'items': self.__items,
        }
    # endregion Utils

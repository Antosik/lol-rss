from typing import Any, Dict, List

from uuid import uuid5, NAMESPACE_URL

from .item import FeedItem
from ..functions.normalize_url import normalize_url


class Feed(object):
    """Feed representation"""

    def __init__(self):
        self.__id = None
        self.__title = None
        self.__description = None
        self.__selfLink = None
        self.__alternateLink = None
        self.__language = None
        self.__authorName = 'Antosik'
        self.__authorUri = 'https://github.com/Antosik'
        self.__ttl = 10
        self.__items = []

    # region Getters & Setters
    def getTTL(self) -> int:
        return self.__ttl

    def getAuthorName(self) -> str:
        return self.__authorName

    def getAuthorUri(self) -> str:
        return self.__authorUri

    def getId(self) -> str:
        return self.__id

    def generateUUID(self, url: str) -> 'Feed':
        self.__id = 'urn:uuid:{0}'.format(uuid5(NAMESPACE_URL, normalize_url(url)))
        return self

    def getTitle(self) -> str:
        return self.__title

    def setTitle(self, title: str) -> 'Feed':
        self.__title = title
        return self

    def getDescription(self) -> str:
        return self.__description

    def setDescription(self, description: str) -> 'Feed':
        self.__description = description
        return self

    def getSelfLink(self) -> str:
        return self.__selfLink

    def setSelfLink(self, selfLink: str) -> 'Feed':
        self.__selfLink = selfLink
        return self

    def getAlternateLink(self) -> str:
        return self.__alternateLink

    def setAlternateLink(self, alternateLink: str) -> 'Feed':
        self.__alternateLink = alternateLink
        return self

    def getLanguage(self) -> str:
        return self.__language

    def setLanguage(self, language: str) -> 'Feed':
        self.__language = language
        return self

    def getItems(self) -> List[FeedItem]:
        return self.__items

    def setItems(self, items: List[FeedItem]) -> 'Feed':
        self.__items = items
        return self
    # endregion Getters & Setters

    def toDict(self) -> Dict[str, Any]:
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

    def reset(self):
        self.__id = None
        self.__title = None
        self.__description = None
        self.__selfLink = None
        self.__alternateLink = None
        self.__language = None
        self.__authorName = 'Antosik'
        self.__authorUri = 'https://github.com/Antosik'
        self.__ttl = 10
        self.__items = []

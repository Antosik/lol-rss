from typing import Any, List, Dict, Union

from datetime import datetime
from uuid import uuid5, NAMESPACE_URL

from ..functions.normalize_url import normalize_url


class FeedItem(object):
    """Feed Item representation"""

    def __init__(self):
        self.__id = None
        self.__title = None
        self.__summary = None
        self.__link = None
        self.__author = None
        self.__createdAt = None
        self.__updatedAt = None
        self.__category = None
        self.__image = None

    # region Getters & Setters
    def getId(self) -> Union[str, None]:
        return self.__id

    def generateUUID(self, url: str) -> 'FeedItem':
        self.__id = 'urn:uuid:{0}'.format(uuid5(NAMESPACE_URL, normalize_url(url)))
        return self

    def getTitle(self) -> Union[str, None]:
        return self.__title

    def setTitle(self, title: str) -> 'FeedItem':
        self.__title = title.replace("\"", "\'")
        return self

    def getSummary(self) -> Union[str, None]:
        return self.__summary

    def setSummary(self, description: str) -> 'FeedItem':
        self.__summary = description.replace("\"", "\'")
        return self

    def getLink(self) -> Union[str, None]:
        return self.__link

    def setLink(self, link: str) -> 'FeedItem':
        self.__link = normalize_url(link)
        return self

    def getAuthor(self) -> Union[str, None]:
        return self.__author

    def setAuthor(self, author: Union[List[str], str]) -> 'FeedItem':
        self.__author = ', '.join(author) if isinstance(author, list) else author
        return self

    def getCreatedAt(self) -> Union[datetime, None]:
        return self.__createdAt

    def setCreatedAt(self, createdAt: datetime) -> 'FeedItem':
        self.__createdAt = createdAt
        return self

    def getUpdatedAt(self) -> Union[datetime, None]:
        return self.__updatedAt

    def setUpdatedAt(self, updatedAt) -> 'FeedItem':
        self.__updatedAt = updatedAt
        return self

    def getCategory(self) -> Union[str, None]:
        return self.__category

    def setCategory(self, category: str) -> 'FeedItem':
        self.__category = category
        return self

    def getImage(self) -> Union[str, None]:
        return self.__image

    def setImage(self, image: str) -> 'FeedItem':
        self.__image = normalize_url(image)
        return self
    # endregion Getters & Setters

    # region Overrides
    def __lt__(self, other):
        return self.getCreatedAt() < other.getCreatedAt()
    # endregion Overrides

    def toDict(self) -> Dict[str, Any]:
        return {
            'id': self.__id,
            'title': self.__title,
            'summary': self.__summary,
            'link': self.__link,
            'author': self.__author,
            'createdAt': self.__createdAt,
            'updatedAt': self.__updatedAt,
            'category': self.__category,
            'image': self.__image
        }

    def reset(self) -> None:
        self.__id = None
        self.__title = None
        self.__summary = None
        self.__link = None
        self.__author = None
        self.__createdAt = None
        self.__updatedAt = None
        self.__category = None
        self.__image = None

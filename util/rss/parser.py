from typing import Any, Dict, List, Optional, Tuple

import feedparser

from ..abstract.feed import Feed, FeedItem
from ..functions.value_by_key import value_by_key


class AtomParser(object):

    # region Parser
    def parse(self, url: str) -> Optional[Feed]:
        """Parse an RSS from URL

        Args:
            url (str): URL of RSS

        Returns:
            Optional[Feed]: Feed or None (if unsuccessful result)
        """
        doc = feedparser.parse(url)

        if not (value_by_key(doc, 'feed') and value_by_key(doc, 'entries')):
            return None

        feed = self.__convertFeedDictToFeed(value_by_key(doc, 'feed'))

        items: List[FeedItem] = []
        for entry in value_by_key(doc, 'entries'):
            items.append(self.__convertFeedItemDictToFeedItem(entry))
        feed.setItems(items)

        return feed
    # endregion Parser

    # region Conversion
    def __convertFeedDictToFeed(self, feed: Dict[str, Any]) -> Feed:
        """Converts a Feed representation from feedparser to abstract Feed

        Args:
            feed (Dict[str, Any]): Feed representation from feedparser

        Returns:
            Feed: Abstract Feed
        """

        result = Feed()

        id = value_by_key(feed, 'id')
        if id:
            result.setId(id)

        title = value_by_key(feed, 'title')
        if title:
            result.setTitle(title)

        description = value_by_key(feed, 'subtitle')
        if description:
            result.setDescription(description)

        selfLink, alternateLink = self.__getSelfAndAlternateLinksForFeed(feed)
        if selfLink:
            result.setSelfLink(selfLink)
        if alternateLink:
            result.setAlternateLink(alternateLink)

        language = value_by_key(feed, 'language')
        if language:
            result.setLanguage(language)

        authorName = value_by_key(feed, 'author_detail.name')
        if authorName:
            result.setAuthorName(authorName)

        authorUri = value_by_key(feed, 'author_detail.href')
        if authorUri:
            result.setAuthorUri(authorUri)

        return result

    def __convertFeedItemDictToFeedItem(self, item: Dict[str, Any]) -> FeedItem:
        """Converts a Feed Entry representation from feedparser to abstract FeedItem

        Args:
            item (Dict[str, Any]): Feed Entry representation from feedparser

        Returns:
            FeedItem: Abstract FeedItem
        """

        result = FeedItem()

        id = value_by_key(item, 'id')
        if id:
            result.setId(id)

        title = value_by_key(item, 'title')
        if title:
            result.setTitle(title)

        summary = value_by_key(item, 'summary')
        if summary:
            result.setSummary(summary)

        author = value_by_key(item, 'author')
        if author:
            result.setAuthor(author)

        createdAt = value_by_key(item, 'published')
        if createdAt:
            result.setCreatedAt(createdAt)

        updatedAt = value_by_key(item, 'updated')
        if updatedAt:
            result.setUpdatedAt(updatedAt)

        category = self.__getCategoryForFeedItem(item)
        if category:
            result.setCategory(category)

        alternateLink, enclosureLink = self.__getAlternateAndEnclosureLinksForFeedItem(item)
        if alternateLink:
            result.setLink(alternateLink)
        if enclosureLink:
            result.setImage(enclosureLink)

        return result
    # endregion Conversion

    # region Utils
    def __getSelfAndAlternateLinksForFeed(self, feed: Dict[str, Any]) -> Tuple[Optional[str], Optional[str]]:
        """Get links: rel="self" and rel="alternate" from feedparser's Feed representation

        Args:
            feed (Dict[str, Any]): Feed representation from feedparser

        Returns:
            Tuple[Optional[str], Optional[str]]: links with rel="self" and rel="alternate"
        """

        links = value_by_key(feed, 'links')
        selfLink = None
        alternateLink = None

        if links and len(links) > 0:
            for link in links:
                if link['rel'] == 'self':
                    selfLink = value_by_key(link, 'href')
                if link['rel'] == 'alternate':
                    alternateLink = value_by_key(link, 'href')

        return (selfLink, alternateLink)

    def __getAlternateAndEnclosureLinksForFeedItem(self, item: Dict[str, Any]) -> Tuple[Optional[str], Optional[str]]:
        """Get links: rel="alternate" and rel="enclosure" from feedparser's FeedEntry representation

        Args:
            item (Dict[str, Any]): FeedEntry representation from feedparser

        Returns:
            Tuple[Optional[str], Optional[str]]: links with rel="alternate" and rel="enclosure"
        """

        links = value_by_key(item, 'links')
        alternateLink = None
        enclosureLink = None

        if links and len(links) > 0:
            for link in links:
                if link['rel'] == 'alternate':
                    alternateLink = value_by_key(link, 'href')
                if link['rel'] == 'enclosure':
                    enclosureLink = value_by_key(link, 'href')

        return (alternateLink, enclosureLink)

    def __getCategoryForFeedItem(self, item: Dict[str, Any]) -> Optional[str]:
        """Get category from feedparser's FeedEntry representation

        Args:
            item (Dict[str, Any]): FeedEntry representation from feedparser

        Returns:
            Optional[str]: Category
        """
        categories = value_by_key(item, 'tags')
        if categories and len(categories) > 0:
            for category in categories:
                return value_by_key(category, 'label')
        return None
    # endregion Utils

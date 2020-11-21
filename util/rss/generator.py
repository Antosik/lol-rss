from feedgen.feed import FeedGenerator as FeedGen, FeedEntry
from pathlib import Path

from ..abstract.feed import Feed, FeedItem


class AtomGenerator(object):

    @staticmethod
    def convertFeedToFeedGen(feed: Feed) -> FeedGen:
        """Convert Feed to feedgen.feed.FeedGenerator

        Args:
            feed (Feed): Feed

        Returns:
            FeedGen: feedgen.feed.FeedGenerator
        """
        feedgen = FeedGen()

        feedgen.ttl(ttl=feed.getTTL())
        feedgen.author(author={
            'name': feed.getAuthorName(),
            'uri': feed.getAuthorUri()
        })

        id = feed.getId()
        if id:
            feedgen.id(id=id)

        title = feed.getTitle()
        if title:
            feedgen.title(title=title)

        description = feed.getDescription()
        if description:
            feedgen.description(description=description)

        language = feed.getLanguage()
        if language:
            feedgen.language(language=language)

        selfLink = feed.getSelfLink()
        if selfLink:
            feedgen.link(link={
                'href': selfLink,
                'rel': 'self'
            })

        alternateLink = feed.getAlternateLink()
        if alternateLink:
            feedgen.link(link={
                'href': alternateLink,
                'rel': 'alternate'
            })

        return feedgen

    @staticmethod
    def convertFeedItemToFeedEntry(item: FeedItem) -> FeedEntry:
        """Convert FeedItem to feedgen.feed.FeedEntry

        Args:
            item (FeedItem): feed item

        Returns:
            FeedEntry: feedgen.feed.FeedEntry
        """
        entry = FeedEntry()

        id = item.getId()
        if id:
            entry.id(id=id)

        title = item.getTitle()
        if title:
            entry.title(title=title)

        summary = item.getSummary()
        if summary:
            entry.summary(summary=summary)

        link = item.getLink()
        if link:
            entry.link(link={
                'href': link,
                'rel': 'alternate'
            })

        author = item.getAuthor()
        if author:
            entry.author(author={
                'name': author
            })

        createdAt = item.getCreatedAt()
        if createdAt:
            entry.pubDate(pubDate=createdAt)

        updatedAt = item.getUpdatedAt()
        if updatedAt:
            entry.updated(updated=updatedAt)

        category = item.getCategory()
        if category:
            entry.category(category={
                'term': category.lower(),
                'label': category
            })

        image = item.getImage()
        if image:
            entry.enclosure(
                url=image,
                type='image/jpg'
            )

        return entry

    def __init__(self, feed: Feed):
        self.__feed = feed

    # region Generator
    def generate(self, filepath: str = "atom.xml") -> None:
        """Generates an RSS file at the given filepath

        Args:
            filepath (str, optional): The path to the file. Defaults to "atom.xml".
        """

        feedgen = self.convertFeedToFeedGen(self.__feed)
        for feeditem in self.__feed.getItems():
            feedgen.add_entry(self.convertFeedItemToFeedEntry(feeditem))

        path = Path(filepath)
        if not path.parent.exists():
            path.parent.mkdir(parents=True)

        feedgen.atom_file(str(path.resolve()))
    # endregion Generator

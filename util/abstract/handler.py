from typing import Any, Dict, Final, List

from util.abstract.feed import Feed
from util.functions.normalize_url import normalize_url
from util.rss.generator import AtomGenerator
from util.rss.parser import AtomParser
from util.s3 import S3


class Handler(object):

    TARGET_DIR: Final = '/tmp/'
    VERSION_DIR: Final = '/v3/'

    def __init__(self):
        """Constructor"""
        self.__s3 = S3()
        self.__generator = AtomGenerator()
        self.__parser = AtomParser()

    def load_servers(self) -> List[Dict[str, Any]]:
        """Abstract method for load servers data to process

        Raises:
            NotImplementedError: Since this is an abstract method - there is no implementation - throw an exception

        Returns:
            List[Dict[str, Any]]: List of servers
        """
        raise NotImplementedError

    def get_filepath(self, server: Dict[str, Any]) -> str:
        """Abstract method for getting file path of RSS generated for server

        Args:
            server (Dict[str, Any]): Server data

        Raises:
            NotImplementedError: Since this is an abstract method - there is no implementation - throw an exception

        Returns:
            str: Path to RSS file
        """
        raise NotImplementedError

    def process_server(self, server: Dict[str, Any]) -> Feed:
        """Abstract method for generating a feed for server

        Args:
            server (Dict[str, Any]): Server data

        Raises:
            NotImplementedError: Since this is an abstract method - there is no implementation - throw an exception

        Returns:
            Feed: Feed from server
        """
        raise NotImplementedError

    def run(self):
        """Run a feed generation process for all service-related servers"""

        servers = self.load_servers()

        for server in servers:

            filepath = normalize_url(self.VERSION_DIR + self.get_filepath(server))
            fullpath = normalize_url(self.TARGET_DIR + filepath)

            selfLink = S3.generate_link(filepath)
            feed = self.process_server(server)
            feed.generateUUID(selfLink)
            feed.setSelfLink(selfLink)

            old_feed = self.__parser.parse(selfLink)

            if old_feed != feed:
                self.__generator.generate(feed, fullpath)
                self.__s3.upload(fullpath, filepath[1:])

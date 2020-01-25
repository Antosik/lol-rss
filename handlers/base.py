import os
import boto3
from feedgen.feed import FeedGenerator
from typing import Dict, Any, List


class RssFeedCollector(object):
    def get_items(self) -> List[Dict[str, any]]:
        raise NotImplementedError

    def filter_item(self, item: Dict[str, Any]) -> bool:
        raise NotImplementedError

    def transform_item(self, item: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError

    def collect(self) -> List:
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


class RssFeedGenerator(object):
    def __init__(self, meta: Dict[str, Any], collector: RssFeedCollector):
        self._collector = collector
        self._meta = meta
        self._s3client = boto3.client('s3')

    def generate(self, filename: str = "rss.xml"):
        """Generates RSS file with given filename that described by meta and contains passed items"""
        fg = FeedGenerator()

        for attr, value in self._meta.items():
            getattr(fg, attr, None)(value)

        fg.author(self._meta['author'], replace=True)
        items = self._collector.collect()

        for item in items:
            fe = fg.add_entry()
            for attr, value in item.items():
                if attr == 'enclosure':
                    getattr(fe, attr, None)(**value)
                else:
                    getattr(fe, attr, None)(value)

        fg.atom_file(filename)

    def uploadToS3(self, filename: str, bucket_name: str = os.environ.get('BUCKET_NAME')) -> Any:
        with open(filename, "rb") as f:
            self._s3client.upload_fileobj(f, bucket_name, os.path.basename(filename))

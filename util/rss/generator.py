import os
import boto3
from feedgen.feed import FeedGenerator
from pathlib import Path
from typing import Any, Dict, Optional

from .collector import RssFeedCollector
from ..functions import normalize_url


class RssFeedGenerator(object):
    """RSS / Atom Generator"""

    @staticmethod
    def selflink_s3(
        object_name: str,
        bucket_name: Optional[str] = os.environ.get('BUCKET_NAME'),
        s3_region: Optional[str] = os.environ.get('S3_REGION')
    ) -> str:
        """Generates a link to the RSS feed in S3

        Arguments:
            object_name {str} -- File path on S3

        Keyword Arguments:
            bucket_name {str} -- Bucket name (default: {os.environ.get('BUCKET_NAME')})
            s3_region {str} -- S3 region (default: {os.environ.get('S3_REGION')})

        Returns:
            [type] -- [description]
        """
        return normalize_url('https://{0}.s3.{1}.amazonaws.com/{2}'.format(bucket_name, s3_region, object_name))

    def __init__(self, meta: Dict[str, Any], collector: RssFeedCollector):
        """Constructor

        Arguments:
            meta {Dict[str, Any]} -- RSS Meta Information
            collector {RssFeedCollector} -- The collector with which we will receive items for RSS
        """
        self._collector = collector
        self._meta = meta
        self._s3client = boto3.client('s3')

    def generate(self, filepath: str = "") -> None:
        """Generates an RSS file with the given name

        Keyword Arguments:
            filename {str} -- The path to the file (default: "rss.xml")
        """

        fg = FeedGenerator()

        for attr, value in self._meta.items():
            getattr(fg, attr, None)(value)

        fg.author(self._meta['author'], replace=True)
        items = self._collector.collect()

        for item in items:
            fe = fg.add_entry()
            for attr, value in item.items():
                if attr == 'enclosure' or attr == 'content':
                    getattr(fe, attr, None)(**value)
                else:
                    getattr(fe, attr, None)(value)

        path = Path(filepath)
        if not path.parent.exists():
            path.parent.mkdir(parents=True)

        fg.atom_file(str(path.resolve()))

    def uploadToS3(self, filepath: str, filename: str, bucket_name: Optional[str] = os.environ.get('BUCKET_NAME')) -> None:
        """Uploads the file with the given name in the S3 bucket

        Arguments:
            filepath {str} -- The path to the file
            filename {str} -- Name of the file

        Keyword Arguments:
            bucket_name {str} -- S3 bucket name (default: {os.environ.get('BUCKET_NAME')})
        """
        self._s3client.upload_file(
            Filename=filepath,
            Bucket=bucket_name,
            Key=filename,
            ExtraArgs={'ContentType': 'application/atom+xml;charset=utf-8'}
        )

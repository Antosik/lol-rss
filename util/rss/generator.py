import os
import boto3
from feedgen.feed import FeedGenerator
from pathlib import Path
from typing import Dict, Any

from .collector import RssFeedCollector
from ..functions import normalize_url


class RssFeedGenerator(object):
    """Генератор RSS/Atom"""

    @staticmethod
    def selflink_s3(
        object_name: str,
        bucket_name: str = os.environ.get('BUCKET_NAME'),
        s3_region: str = os.environ.get('S3_REGION')
    ):
        """Генерирует ссылку на сам RSS-feed в S3

        Arguments:
            object_name {str} -- путь к файлу на S3

        Keyword Arguments:
            bucket_name {str} -- имя bucket'a (default: {os.environ.get('BUCKET_NAME')})
            s3_region {str} -- s3 регион (default: {os.environ.get('S3_REGION')})

        Returns:
            [type] -- [description]
        """
        return normalize_url('https://{0}.s3.{1}.amazonaws.com/{2}'.format(bucket_name, s3_region, object_name))

    def __init__(self, meta: Dict[str, Any], collector: RssFeedCollector):
        """Конструктор класса

        Arguments:
            meta {Dict[str, Any]} -- Мета-информация о RSS
            collector {RssFeedCollector} -- Коллектор, с помощью которого мы будем получать элементы для RSS
        """
        self._collector = collector
        self._meta = meta
        self._s3client = boto3.client('s3')

    def generate(self, filepath: str = "") -> None:
        """Генерирует RSS файл с заданным именем

        Keyword Arguments:
            filename {str} -- путь к файлу (default: "rss.xml")
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

    def uploadToS3(self, filepath: str, filename: str, bucket_name: str = os.environ.get('BUCKET_NAME')) -> None:
        """Загружает файл с заданным именем в S3 bucket

        Arguments:
            filepath {str} -- путь к файлу
            filename {str} -- имя файла

        Keyword Arguments:
            bucket_name {str} -- имя bucket'a в S3 (default: {os.environ.get('BUCKET_NAME')})
        """
        self._s3client.upload_file(
            Filename=filepath,
            Bucket=bucket_name,
            Key=filename,
            ExtraArgs={'ContentType': 'application/atom+xml;charset=utf-8'}
        )

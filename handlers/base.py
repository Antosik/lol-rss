import os
import boto3
from feedgen.feed import FeedGenerator
from typing import Dict, Any, List


class RssFeedCollector(object):
    """Базовый класс для получения, фильтрации и трансформирования данных в пригодный для RSS"""

    def get_items(self) -> List[Dict[str, any]]:
        """Абстрактный метод для получения данных

        Raises:
            NotImplementedError: Так как это абстрактный метод - нет реализации - выбрасываем исключение

        Returns:
            List[Dict[str, any]] -- Список с элементами
        """
        raise NotImplementedError

    def filter_item(self, item: Dict[str, Any]) -> bool:
        """Абстрактный метод для фильтрации элементов

        Arguments:
            item {Dict[str, Any]} -- Элемент для фильтрации

        Raises:
            NotImplementedError: Так как это абстрактный метод - нет реализации - выбрасываем исключение

        Returns:
            bool -- Оставляем элемент в списке (True) или убираем (False)
        """
        raise NotImplementedError

    def transform_item(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """Абстрактный метод для трансформирования элементов в пригодный для RSS/Atom

        Arguments:
            item {Dict[str, Any]} -- Элемент для трансформирования

        Raises:
            NotImplementedError: Так как это абстрактный метод - нет реализации - выбрасываем исключение

        Returns:
            Dict[str, Any] -- Трансформированный элемент
        """

        raise NotImplementedError

    def collect(self) -> List[Dict[str, Any]]:
        """Метод, вызывающий получение, фильтрацию и последующую трансформацию элементов

        Returns:
            List[Dict[str, Any]] -- Список элементов, пригодный для RSS/Atom
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


class RssFeedGenerator(object):
    """Генератор RSS/Atom"""

    def __init__(self, meta: Dict[str, Any], collector: RssFeedCollector):
        """Конструктор класса

        Arguments:
            meta {Dict[str, Any]} -- Мета-информация о RSS
            collector {RssFeedCollector} -- Коллектор, с помощью которого мы будем получать элементы для RSS
        """
        self._collector = collector
        self._meta = meta
        self._s3client = boto3.client('s3')

    def generate(self, filename: str = "rss.xml") -> None:
        """Генерирует RSS файл с заданным именем

        Keyword Arguments:
            filename {str} -- имя файла (default: {"rss.xml"})
        """

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

    def uploadToS3(self, filename: str, bucket_name: str = os.environ.get('BUCKET_NAME')) -> None:
        """Загружает файл с заданным именем в S3 bucket

        Arguments:
            filename {str} -- имя файла

        Keyword Arguments:
            bucket_name {str} -- имя bucket'a в S3 (default: {os.environ.get('BUCKET_NAME')})
        """
        with open(filename, "rb") as f:
            self._s3client.upload_fileobj(
                f, bucket_name, os.path.basename(filename))

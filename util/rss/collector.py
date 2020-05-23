import uuid
from typing import Dict, Any, List


class RssFeedCollector(object):
    """Базовый класс для получения, фильтрации и трансформирования данных в пригодный для RSS"""

    @staticmethod
    def uuid_item(url: str) -> str:
        """Генерация уникального id для каждого элемента

        Arguments:
            url {str} -- url, идентифицирующий элемент

        Returns:
            str -- сгенерированный id
        """
        return uuid.uuid5(uuid.NAMESPACE_URL, url)

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

import requests
from typing import Dict, Any, List, Tuple

from base import RssFeedCollector, RssFeedGenerator


class LOLSalesCollector(RssFeedCollector):
    """Получение данных о скидках на чемпионов и образы"""

    def get_items(self) -> List[Dict[str, any]]:
        """Получаем скидки с API"""
        response = requests.get(
            url='https://store.ru.lol.riotgames.com/storefront/v1/catalog?region=RU&language=ru_RU',
        )
        response.raise_for_status()
        return response.json()

    def filter_item(self, item: Dict[str, Any]) -> bool:
        """Возвращаем только скидки"""
        return item.get('sale')

    def transform_item(self, item: Tuple[str, Dict[str, Any]]) -> Dict[str, Any]:
        """Приводим к виду, удобному для генератора RSS"""

        """Пары "ключ - текст" для типов элементов (образы, чемпионы, ...)"""
        sale_type_map = {
            'CHAMPION_SKIN': 'Скидки на образы',
            'CHAMPION': 'Скидки на чемпионов'
        }

        def findRPCost(prices):
            """Находим цену в RP"""
            return next(price for price in prices if price['currency'] == 'RP')

        def firstTransformItem(item):
            """Приводим элемент к первой форме - чтобы можно было отсортировать по скидке"""
            name = item['localizations']['ru_RU']['name']
            discount_price = findRPCost(item['sale']['prices'])
            discount = round(discount_price['discount'] * 100)
            return {'name': name, 'discount': discount, 'cost': discount_price['cost']}

        def secondTransformItem(item):
            """Приводим элемент ко второй форме - строка"""
            return '- {0} - {1}RP (-{2}%) \n'.format(item['name'], item['cost'], item['discount'])

        key, items = item

        formatted_items = list(map(lambda x: firstTransformItem(x), items))
        formatted_items.sort(key=(lambda x: x['discount']), reverse=True)

        sale_type = items[0]['inventoryType']
        sale_start = items[0]['sale']['startDate']

        uuid = RssFeedCollector.uuid_item('https://store.ru.lol.riotgames.com/storefront/v1/catalog?region=RU&language=ru_RU&id={0}'.format(key))
        title = sale_type_map[sale_type]
        description = ''.join(
            list(map(lambda x: secondTransformItem(x), formatted_items)))

        return {
            'id': 'urn:uuid:{0}'.format(uuid),
            'title': title,
            'description': description,
            'link': {'href': 'https://ru.leagueoflegends.com/ru-ru/', 'rel': 'alternate'},
            'author': {'name': 'Riot Games'},
            'pubDate': sale_start,
        }

    def collect(self) -> List:
        """Переопределяем метод, так как нам нужно группировать элементы по дате начала скидки"""
        items = self.get_items()
        results = {}

        for item in items:
            if self.filter_item(item):
                sale_start = item['sale']['endDate']
                item_type = item['inventoryType']
                key = '{0}-{1}'.format(sale_start[:10], item_type)

                if not results.get(key):
                    results[key] = []

                results[key].append(item)

        return list(map(lambda x: self.transform_item(x), results.items()))


def handle(event={}, context={}):
    """Обработчик для AWS Lambda"""

    collector = LOLSalesCollector()

    filename = 'lolsales.xml'
    filepath = '/tmp/' + filename
    selflink = RssFeedGenerator.selflink_s3(filename)

    generator = RssFeedGenerator(
        meta={
            'id': selflink,
            'title': 'LoL Скидки [RU]',
            'description': 'Еженедельные скидки на чемпионов и скины',
            'link': [
                {
                    'href': selflink,
                    'rel': 'self'
                },
                {
                    'href': 'https://ru.leagueoflegends.com/ru-ru/',
                    'rel': 'alternate'
                }
            ],
            'author': {'name': 'Antosik', 'uri': 'https://github.com/Antosik'},
            'language': 'ru',
            'ttl': 15
        },
        collector=collector
    )

    generator.generate(filepath)
    generator.uploadToS3(filepath, filename)

    return 'ok'

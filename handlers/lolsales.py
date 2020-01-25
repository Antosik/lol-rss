import json
import requests
from typing import Dict, Any, List, Tuple

from base import RssFeedCollector, RssFeedGenerator


class LOLSalesCollector(RssFeedCollector):
    def get_items(self) -> List[Dict[str, any]]:
        response = requests.get(
            url='https://store.ru.lol.riotgames.com/storefront/v1/catalog?region=RU&language=ru_RU',
        )
        response.raise_for_status()
        return response.json()

    def filter_item(self, item: Dict[str, Any]) -> bool:
        return item.get('sale')

    def transform_item(self, item: Tuple[str, Dict[str, Any]]) -> Dict[str, Any]:
        """Map beetween 'inventoryType' and its description"""
        sale_type_map = {
            'CHAMPION_SKIN': 'Скидки на скины',
            'CHAMPION': 'Скидки на чемпионов'
        }

        def findRPCost(prices):
            return next(price for price in prices if price['currency'] == 'RP')

        def firstTransformItem(item):
            name = item['localizations']['ru_RU']['name']
            discount_price = findRPCost(item['sale']['prices'])
            discount = round(100 - discount_price['discount'] * 100)
            return { 'name': name, 'discount': discount, 'cost': discount_price['cost'] }
        
        def secondTransformItem(item):
            return '- {0} - {1}RP (-{2}%) \n'.format(item['name'], item['cost'], item['discount'])
        
        key, items = item

        formatted_items = list(map(lambda x: firstTransformItem(x), items))
        formatted_items.sort(key=(lambda x: x['discount']), reverse=True)

        sale_type = items[0]['inventoryType']
        sale_start = items[0]['sale']['startDate']

        title = sale_type_map[sale_type]
        description = ''.join(list(map(lambda x: secondTransformItem(x), formatted_items)))

        return {
            'id': key,
            'title': title,
            'description': description,
            'link': {'href': 'https://ru.leagueoflegends.com/ru-ru/', 'rel': 'alternate'},
            'author': {'name': 'Riot Games'},
            'pubDate': sale_start,
        }

    def collect(self) -> List:
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

def handle(event, context):
    collector = LOLSalesCollector()

    generator = RssFeedGenerator(
        meta={
            'id': 'antosik:rulolsales',
            'title': 'LoL Скидки [RU]',
            'description': 'Еженедельные скидки на чемпионов и скины',
            'link': {'href': 'https://ru.leagueoflegends.com/ru-ru/', 'rel': 'alternate'},
            'author': {'name':'Antosik', 'uri':'https://github.com/Antosik'},
            'language': 'ru',
            'ttl': 15
        },
        collector=collector
    )

    filename = '/tmp/lolsales.xml'

    generator.generate(filename)
    generator.uploadToS3(filename)
    
    return 'ok'
    
handle({},{})
import requests
from typing import Dict, Any, List

from base import RssFeedCollector, RssFeedGenerator


class LOLeSportsCollector(RssFeedCollector):
    """Получение данных с официального сайта Лиги - ru.leagueoflegends.com/ru-ru/news"""

    def get_items(self) -> List[Dict[str, any]]:
        """Получаем новости с сайта"""
        response = requests.get(
            url='https://lolstatic-a.akamaihd.net/frontpage/apps/prod/harbinger-l10-website/ru-ru/master/ru-ru/page-data/latest-news/page-data.json',
        )
        response.raise_for_status()
        data = response.json()

        def findNewsSection(sections):
            return next(section for section in sections if section['type'] == 'category_article_list_contentstack')

        data = response.json()['result']['pageContext']['data']['sections']
        return findNewsSection(data)['props']['articles']

    def filter_item(self, item: Dict[str, Any]) -> bool:
        """Возвращаем все элементы - нет фильтра"""
        return True

    def transform_item(self: RssFeedCollector, item: Dict[str, Any]) -> Dict[str, Any]:
        """Приводим к виду, удобному для генератора RSS"""

        def transform_item_link(link: Dict[str, str]) -> str:
            """Преобразование внутренней и внешней ссылки"""
            if link['internal']:
                return 'https://ru.leagueoflegends.com/ru-ru/{0}'.format(link['url'])
            else:
                return link['url']

        author = list(map(lambda x: {'name': x}, item['authors']))
        link = transform_item_link(item['link'])
        category = {
            'term': 'category',
            'label': item['category']
        }

        result = {
            'id': item['id'],
            'title': item['title'],
            'link': {'href': link, 'rel': 'alternate'},
            'author': author,
            'pubDate': item['date'],
            'category': category
        }

        if item['imageUrl']:
            result['enclosure'] = {
                'url': item['imageUrl'],
                'length': 0,
                'type': 'image/jpg'
            }
        return result


def handle(event={}, context={}):
    """Обработчик для AWS Lambda"""

    collector = LOLeSportsCollector()

    generator = RssFeedGenerator(
        meta={
            'id': 'antosik:rulolnews',
            'title': 'LoL Новости [RU]',
            'description': 'Новости и обновления игры',
            'link': {
                'href': 'https://ru.leagueoflegends.com/ru-ru/news/',
                'rel': 'alternate'
            },
            'author': {
                'name': 'Antosik',
                'uri': 'https://github.com/Antosik'
            },
            'language': 'ru',
            'ttl': 15
        },
        collector=collector
    )

    filename = '/tmp/lolnews.xml'

    generator.generate(filename)
    generator.uploadToS3(filename)

    return 'ok'

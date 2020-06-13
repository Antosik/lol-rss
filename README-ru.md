[![Serverless Framework](https://img.shields.io/badge/-serverless%20%E2%9A%A1-%23000)](http://www.serverless.com) 
[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/Antosik/lol-rss/Python%20checks)](https://github.com/Antosik/lol-rss/actions)

[English version (EN)](https://github.com/Antosik/lol-rss/blob/master/README.md)

## Описание
Данный сервис генерирует RSS из различных официальных источников новостей о [League of Legends](https://leagueoflegends.com/), [Valorant](https://playvalorant.com/) и [Legends of Runeterra](https://playruneterra.com/)

## Как пользоваться

-   Использовать RSS-агрегатор, например, [Feedly](https://feedly.com/)
-   Интегрировать с [Zapier](https://zapier.com/), [Integromat](https://www.integromat.com/) или другими сервисами автоматизации процессов
    -   Гайды по интеграции с Zapier - [Lite](https://github.com/Antosik/lol-rss/wiki/Zapier-%5BRU%5D) и [Advanced](https://github.com/Antosik/lol-rss/wiki/Zapier-%5BRU%5D-%5BAdvanced%5D)

## Поддерживаемые сервисы

-   [League of Legends](https://github.com/Antosik/lol-rss/wiki/League-of-Legends-%5BRU%5D)
    -   Новости
    -   Новости киберспорта
    -   Статус сервера
-   [Valorant](https://github.com/Antosik/lol-rss/wiki/Valorant-%5BRU%5D)
    -   Новости
    -   Статус сервера
-   [Legends of Runeterra](https://github.com/Antosik/lol-rss/wiki/Legends-of-Runeterra-%5BRU%5D)
    -   Статус сервера

## Как это работает

Весь код написан на [Python](https://www.python.org/) и вызывается в [AWS Lambda](https://aws.amazon.com/ru/lambda/) каждые 15 минут.  
В процессе мы запрашиваем информацию из [наших источников](#Поддерживаемые-сервисы), генерируем из нее RSS-фид и загружаем его на [AWS S3](https://aws.amazon.com/ru/s3/)

## Используемые библиотеки

-   [requests](https://github.com/psf/requests/) - для HTTP-запросов
-   [feedgen](https://github.com/lkiesow/python-feedgen) - для генерации RSS/Atom
-   [boto3](https://github.com/boto/boto3) - для загрузки файлов на S3
-   [serverless](https://serverless.com/) - для удобного развертывания на AWS

## Соответствие стандарту

![Valid Atom 1.0 feed](https://validator.w3.org/feed/images/valid-atom.png)  
Все генерируемые RSS-фиды были провалидированы при помощи [W3C Feed Validation Service](https://validator.w3.org/feed/) и являются валидными Atom 1.0 фидами.

## Attribution

This service isn't developed by Riot Games and doesn't reflect the views or opinions of Riot Games or anyone officially involved in producing or managing League of Legends, Valorant or Legends of Runeterra. League of Legends, Valorant, Legends of Runeterra, and Riot Games are trademarks or registered trademarks of Riot Games, Inc. League of Legends, Valorant, Legends of Runeterra (c) Riot Games, Inc.

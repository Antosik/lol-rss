# LoL RSS Serverless Service

Генератор RSS из различных источников новостей о [League of Legends](https://ru.leagueoflegends.com/ru-ru/)

## Поддерживаемые сервисы
### Новости и обновления LoL'a
Главный источник новостей, списков обновлений и многого другого  

Ссылки:
  - [RSS](https://antosik-lol-rss.s3.eu-central-1.amazonaws.com/lolnews.xml)
  - [Источник](https://ru.leagueoflegends.com/ru-ru/latest-news/)
  - [Исходный код](https://github.com/Antosik/lol-rss/blob/master/handlers/lolnews.py)

### Киберспорт
Новости и статьи из киберспортивного мира Лиги Легенд  

Ссылки:
  - [RSS](https://antosik-lol-rss.s3.eu-central-1.amazonaws.com/lolesports.xml)
  - [Источник](https://ru.lolesports.com/articles)
  - [Исходный код](https://github.com/Antosik/lol-rss/blob/master/handlers/lolesports.py)

### Статус сервера
Информация о планируемых технических обслуживаниях сервера и внезапно возникших неполадках  

Ссылки:
  - [RSS](https://antosik-lol-rss.s3.eu-central-1.amazonaws.com/lolstatus.xml)
  - [Источник](https://status.riotgames.com/?region=ru&locale=ru_RU&product=leagueoflegends)
  - [Исходный код](https://github.com/Antosik/lol-rss/blob/master/handlers/lolstatus.py)

  
### Скидки в магазине
Публикуем скидки на чемпионов и скины  

Ссылки:
  - [RSS](https://antosik-lol-rss.s3.eu-central-1.amazonaws.com/lolsales.xml)
  - [Исходный код](https://github.com/Antosik/lol-rss/blob/master/handlers/lolsales.py)

## Как это работает
Весь код написан на [Python](https://www.python.org/) и гоняется на [AWS Lambda](https://aws.amazon.com/ru/lambda/) каждые 15 минут.  
В ходе выполнения мы запрашиваем информацию из [наших источников](#Поддерживаемые-сервисы), генерируем из нее RSS-фид и загружаем его на [AWS S3](https://aws.amazon.com/ru/s3/).

## Используемые библиотеки
- [requests](https://github.com/psf/requests/) - для HTTP-запросов
- [feedgen](https://github.com/lkiesow/python-feedgen) - для генерации RSS/Atom
- [boto3](https://github.com/boto/boto3) - для загрузки файлов на S3

## Разное
Все генерируемые RSS-фиды были провалидированы при помощи [W3C Feed Validation Service](https://validator.w3.org/feed/) и являются валидными Atom 1.0 фидами - ![Valid Atom 1.0 feed](https://validator.w3.org/feed/images/valid-atom.png).


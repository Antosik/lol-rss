[![Serverless Framework](https://img.shields.io/badge/-serverless%20%E2%9A%A1-%23000)](http://www.serverless.com) 
[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/Antosik/lol-rss/Python%20checks)](https://github.com/Antosik/lol-rss/actions)


[Версия на русском (RU)](https://github.com/Antosik/lol-rss/blob/master/README-ru.md)

## Description

This service generates RSS from various official news sources about [League of Legends](https://leagueoflegends.com/), [Valorant](https://playvalorant.com/), [Legends of Runeterra](https://playruneterra.com/) and [Wild Rift](https://wildrift.leagueoflegends.com/)

## How to use

-   Use RSS aggregator, e.g. [Feedly](https://feedly.com/)
-   Integrate with [Zapier](https://zapier.com/), [Integromat](https://www.integromat.com/) or other process automation services
    -   Zapier Integration Guides - [Lite](https://github.com/Antosik/lol-rss/wiki/Zapier) and [Advanced](https://github.com/Antosik/lol-rss/wiki/Zapier-%5BAdvanced%5D)

## Supported Services

-   [League of Legends](https://github.com/Antosik/lol-rss/wiki/League-of-Legends)
    -   News
    -   Server status
-   [Valorant](https://github.com/Antosik/lol-rss/wiki/Valorant)
    -   News
    -   Server status
-   [Legends of Runeterra](https://github.com/Antosik/lol-rss/wiki/Legends-of-Runeterra)
    -   Server status
-   [Wild Rift](https://github.com/Antosik/lol-rss/wiki/Wild-Rift)
    -   News
    -   Server status

## How it works

All code is written in [Python](https://www.python.org/) and called in [AWS Lambda](https://aws.amazon.com/lambda/) every 10 minutes.
In the process, we request information from [our sources](#Supported-Services), generate an RSS feed from it and upload it to [AWS S3](https://aws.amazon.com/s3/)

## Libraries used

-   [requests](https://github.com/psf/requests/) - for HTTP requests
-   [feedgen](https://github.com/lkiesow/python-feedgen) - for generating RSS / Atom
-   [feedparser](https://github.com/kurtmckee/feedparser) - for parsing RSS / Atom
-   [boto3](https://github.com/boto/boto3) - to upload files to S3
-   [serverless](https://serverless.com/) - for easy deployment on AWS

## Compliance with the standard

![Valid Atom 1.0 feed](https://validator.w3.org/feed/images/valid-atom.png)  
All generated RSS feeds were provided using the [W3C Feed Validation Service](https://validator.w3.org/feed/) and are valid Atom 1.0 feeds.

## Attribution

This service isn't developed by Riot Games and doesn't reflect the views or opinions of Riot Games or anyone officially involved in producing or managing League of Legends, Valorant, Legends of Runeterra or Wild Rift. League of Legends, Valorant, Legends of Runeterra, Wild Rift and Riot Games are trademarks or registered trademarks of Riot Games, Inc. League of Legends, Valorant, Legends of Runeterra, Wild Rift (c) Riot Games, Inc.

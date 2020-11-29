from tests.helpers.mock_response import MockResponse


def mocked_success_get(*args, **kwargs):
    raw_response = {
        "result": {
            "data": {
                "allContentstackNews": {
                    "nodes": []
                },
                "allContentstackArticles": {
                    "articles": [
                        {
                            "id": "RandomId",
                            "title": "Random Title",
                            "description": "Random Description",
                            "link": {
                                "url": "/news/random-post/"
                            },
                            "date": "11-11-2020",
                            "featuredImage": {
                                "focalPoint": "Top",
                                "banner": {
                                    "url": "https://example.com"
                                }
                            },
                            "categories": [
                                {
                                    "title": "Random Category"
                                }
                            ],
                            "youtubeLink": "",
                            "externalLink": ""
                        },
                    ]
                }
            }
        }
    }

    return MockResponse(raw_response, 200)

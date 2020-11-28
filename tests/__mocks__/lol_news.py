from tests.helpers.mock_response import MockResponse


def mocked_success_get(*args, **kwargs):
    raw_response = {
        "result": {
            "pageContext": {
                "data": {
                    "sections": [
                        {
                            "type": "category_intro"
                        },
                        {
                            "type": "category_article_list_contentstack",
                            "props": {
                                "articles": [
                                    {
                                        "id": "randomId",
                                        "link": {
                                            "url": "/news/random-post/",
                                            "internal": True
                                        },
                                        "category": "Random Category",
                                        "title": "Random Title",
                                        "authors": [
                                            "Random Author"
                                        ],
                                        "date": "2020-11-23T18:00:00.000Z",
                                        "imageUrl": "https://example.com"
                                    }
                                ]
                            }
                        }
                    ]
                }
            }
        }
    }

    return MockResponse(raw_response, 200)

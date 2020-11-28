from tests.helpers.mock_response import MockResponse


def mocked_success_get(*args, **kwargs):
    raw_response = {
        "result": {
            "data": {
                "allContentstackArticles": {
                    "nodes": [
                        {
                            "banner": {
                                "url": "https://example.com"
                            },
                            "date": "2020-11-25T12:00:00.000Z",
                            "description": "Random Description",
                            "title": "Random Title",
                            "id": "Random Id",
                            "external_link": "",
                            "url": {
                                "url": "/news/random-post/"
                            }
                        }
                    ]
                }
            }
        }
    }

    return MockResponse(raw_response, 200)

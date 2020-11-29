from tests.helpers.mock_response import MockResponse


def mocked_success_get(*args, **kwargs):
    raw_response = {
        "id": "random",
        "maintenances": [
            {
                "id": 1,
                "updates": [
                    {
                        "id": 2,
                        "publish": True,
                        "translations": [
                            {
                                "content": "Lorem Ipsum",
                                "locale": "en_US"
                            },
                            {
                                "content": "Random Text",
                                "locale": "randomLocale"
                            }
                        ],
                        "created_at": "2020-11-08T01:25:00.434856+00:00",
                        "author": "Random Author",
                        "updated_at": "2020-11-09T12:00:00+00:00"
                    }
                ],
                "created_at": "2020-11-08T01:25:00.404387+00:00",
                "titles": [
                    {
                        "content": "Lorem Ipsum",
                        "locale": "notRandomLocale"
                    },
                    {
                        "content": "Random Title",
                        "locale": "en_US"
                    }
                ],
                "maintenance_status": "scheduled",
                "updated_at": None
            }
        ],
        "incidents": []
    }

    return MockResponse(raw_response, 200)

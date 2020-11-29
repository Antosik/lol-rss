from tests.helpers.mock_response import MockResponse


def mocked_success_get(*args, **kwargs):
    raw_response = [
        {
            "id": 1,
            "title": "Random Title",
            "nick_name": "Random Author",
            "full_content": "",
            "published": True,
            "original": "https://example.com",
            "published_at": "2020-11-25T17:04:11.457Z",
            "created_at": "2020-11-25T10:13:43.073Z",
            "updated_at": "2020-11-25T17:04:24.011Z"
        }
    ]

    return MockResponse(raw_response, 200)

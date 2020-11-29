from requests import HTTPError


class MockResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data

    def raise_for_status(self):
        if self.status_code > 400:
            raise HTTPError


def mocked_unsuccessful_get(*args, **kwargs):
    return MockResponse({}, 200)


def mocked_notfound_get(*args, **kwargs):
    return MockResponse(None, 404)

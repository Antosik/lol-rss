import unittest

from util.functions.normalize_url import normalize_url


class TestNormalizeURL(unittest.TestCase):
    def test_correct_url(self):
        """
        Test that correct url is the same after normalize
        """
        url = 'https://www.google.com/'
        result = normalize_url(url)
        self.assertEqual(result, url)

    def test_slashes(self):
        """
        Test normalize for url with extra slashes
        """
        url = 'https://www.random.url///qwerty///'
        result = normalize_url(url)
        self.assertEqual(result, 'https://www.random.url/qwerty/')

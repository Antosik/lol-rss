from urllib.parse import urlparse, urlunparse, quote


def normalize_url(url):
    parts = urlparse(url)
    return urlunparse(parts._replace(path=quote(parts.path).replace("//", "/")))

from urllib.parse import urlparse, urlunparse, quote


def normalize_url(url):
    parts = urlparse(url)

    path = quote(parts.path)
    while '//' in path:
        path = path.replace("//", "/")

    return urlunparse(parts._replace(path=path))

from urllib.parse import quote, urlparse, urlunparse


def normalize_url(url: str) -> str:
    """Normalize url - strip extra slashes

    Args:
        url (str): URL to normalize

    Returns:
        str: Normalized URL
    """
    parts = urlparse(url)

    path = quote(parts.path)
    while '//' in path:
        path = path.replace("//", "/")

    return urlunparse(parts._replace(path=path))

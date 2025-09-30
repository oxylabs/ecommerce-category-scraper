from urllib.parse import urljoin, urlparse


def normalize_url(host_url: str, href_url: str) -> str:
    if not href_url:
        return host_url

    parsed_href = urlparse(href_url)
    if parsed_href.scheme and parsed_href.netloc:
        return href_url

    return urljoin(host_url, href_url)

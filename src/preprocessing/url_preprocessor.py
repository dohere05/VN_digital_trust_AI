from urllib.parse import urlparse

def normalize_url(url: str) -> str:
    url = (url or "").strip()
    if not url:
        return ""
    if "://" not in url:
        url = "http://" + url
    return url

def parse_url(url: str):
    return urlparse(normalize_url(url))

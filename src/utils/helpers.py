import re
import unicodedata
from urllib.parse import urlparse

URL_PATTERN = re.compile(r"""(?i)\b((?:https?://|www\.)[^\s<>"']+)""")

def normalize_whitespace(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "")).strip()

def normalize_unicode(text: str) -> str:
    return unicodedata.normalize("NFC", text or "")

def extract_urls(text: str) -> list[str]:
    found = URL_PATTERN.findall(text or "")
    cleaned = []
    for url in found:
        cleaned.append(url.rstrip(".,;:!?)]}"))
    return list(dict.fromkeys(cleaned))

def get_domain(value: str) -> str:
    value = (value or "").strip()
    if not value:
        return ""
    parsed = urlparse(value if "://" in value else f"//{value}", scheme="")
    host = parsed.hostname or ""
    return host.lower().rstrip(".")

from urllib.parse import urlparse
from src.preprocessing.url_preprocessor import normalize_url
from src.services.dns_service import has_dns_record

def validate_url(url: str) -> dict:
    normalized = normalize_url(url)
    try:
        parsed = urlparse(normalized)
        domain = parsed.hostname or ""
        valid_syntax = bool(parsed.scheme in ("http", "https") and domain)
        return {
            "valid_syntax": valid_syntax,
            "normalized": normalized,
            "scheme": parsed.scheme,
            "domain": domain,
            "https": parsed.scheme == "https",
            "dns_exists": has_dns_record(domain) if valid_syntax else False,
        }
    except Exception:
        return {
            "valid_syntax": False,
            "normalized": normalized,
            "scheme": None,
            "domain": None,
            "https": False,
            "dns_exists": False,
        }

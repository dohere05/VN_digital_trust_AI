import ipaddress
import math
import re
from urllib.parse import urlparse

SUSPICIOUS_TOKENS = (
    "login", "verify", "verification", "account", "secure", "update",
    "password", "bank", "otp", "prize", "free", "gift",
    "dang-nhap", "xac-minh", "tai-khoan", "nhan-qua"
)

def _is_ip(host: str) -> int:
    try:
        ipaddress.ip_address(host)
        return 1
    except ValueError:
        return 0

def extract_url_features(url: str) -> dict:
    raw = (url or "").strip()
    normalized = raw if "://" in raw else f"http://{raw}"
    parsed = urlparse(normalized)
    host = (parsed.hostname or "").lower()
    path = parsed.path or ""
    query = parsed.query or ""

    return {
        "url_length": len(raw),
        "host_length": len(host),
        "path_length": len(path),
        "query_length": len(query),
        "dot_count": raw.count("."),
        "hyphen_count": raw.count("-"),
        "digit_count": sum(c.isdigit() for c in raw),
        "at_count": raw.count("@"),
        "percent_count": raw.count("%"),
        "subdomain_count": max(0, host.count(".") - 1),
        "uses_https": int(parsed.scheme.lower() == "https"),
        "host_is_ip": _is_ip(host),
        "suspicious_token_count": sum(token in raw.lower() for token in SUSPICIOUS_TOKENS),
        "has_punycode": int("xn--" in host),
        "entropy_proxy": round(len(set(raw)) / max(1, len(raw)), 6),
    }

import re
from src.services.hotline_service import load_hotlines

def normalize_sender(sender: str) -> str:
    return re.sub(r"\D+", "", sender or "")

def validate_hotline(sender: str) -> dict:
    normalized = normalize_sender(sender)
    if not normalized:
        return {
            "provided": False,
            "verified": False,
            "normalized": "",
            "organization": None,
            "category": None,
            "source": None,
        }

    record = load_hotlines().get(normalized)
    if not record:
        return {
            "provided": True,
            "verified": False,
            "normalized": normalized,
            "organization": None,
            "category": None,
            "source": None,
        }

    return {
        "provided": True,
        "verified": bool(record.get("verified", False)),
        "normalized": normalized,
        "organization": record.get("organization"),
        "category": record.get("category"),
        "source": record.get("source"),
    }

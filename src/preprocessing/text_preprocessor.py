import re
from src.utils.helpers import normalize_unicode, normalize_whitespace

URL_RE = re.compile(r"https?://\S+|www\.\S+", re.IGNORECASE)
EMAIL_RE = re.compile(r"\b[\w.\-+]+@[\w.\-]+\.\w+\b", re.IGNORECASE)
PHONE_RE = re.compile(r"(?<!\d)(?:\+?84|0)?[\d .\-]{8,14}(?!\d)")

def clean_text(text: str, keep_url_token: bool = True) -> str:
    text = normalize_unicode(text).lower()
    text = EMAIL_RE.sub(" EMAIL ", text)
    text = URL_RE.sub(" URL " if keep_url_token else " ", text)
    text = PHONE_RE.sub(" PHONE ", text)
    text = re.sub(r"[^\wÀ-ỹ\s!?$%]", " ", text, flags=re.UNICODE)
    return normalize_whitespace(text)

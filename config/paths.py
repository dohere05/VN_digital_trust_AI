from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]

ASSETS_DIR = BASE_DIR / "assets"
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
SAMPLES_DIR = DATA_DIR / "samples"
MODELS_DIR = BASE_DIR / "models"

SPAM_MODEL_DIR = MODELS_DIR / "spam"
FAKE_MODEL_DIR = MODELS_DIR / "fake_news"
URL_MODEL_DIR = MODELS_DIR / "malicious_url"

REFERENCE_DIR = RAW_DATA_DIR / "reference"
OFFICIAL_HOTLINES_FILE = REFERENCE_DIR / "official_hotlines.json"
DISPOSABLE_EMAIL_FILE = REFERENCE_DIR / "disposable_email_domains.txt"
SUSPICIOUS_KEYWORDS_FILE = REFERENCE_DIR / "suspicious_keywords_vi.json"

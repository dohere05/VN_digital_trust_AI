import json
from config.paths import OFFICIAL_HOTLINES_FILE

def load_hotlines() -> dict:
    try:
        data = json.loads(OFFICIAL_HOTLINES_FILE.read_text(encoding="utf-8"))
        return data.get("hotlines", {})
    except Exception:
        return {}

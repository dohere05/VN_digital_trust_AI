from functools import lru_cache
from pathlib import Path
import joblib

@lru_cache(maxsize=16)
def load_joblib(path: str):
    p = Path(path)
    if not p.exists():
        return None
    return joblib.load(p)

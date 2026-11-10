from pathlib import Path
import pandas as pd

def load_csv(path: str | Path) -> pd.DataFrame:
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Không tìm thấy dataset: {path}")
    return pd.read_csv(path)

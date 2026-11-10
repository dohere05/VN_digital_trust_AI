from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

from config.paths import RAW_DATA_DIR, URL_MODEL_DIR
from src.preprocessing.feature_extractor import extract_url_features
from train.common.dataset_loader import load_csv
from train.common.metrics import classification_metrics
from train.common.model_utils import save_joblib, save_json

DATASET = RAW_DATA_DIR / "malicious_url" / "urls.csv"

def normalize_label(value):
    text = str(value).strip().lower()
    if text in {"1", "malicious", "phishing", "bad", "unsafe"}:
        return 1
    if text in {"0", "safe", "benign", "good"}:
        return 0
    raise ValueError(f"Nhãn không hỗ trợ: {value}")

def main():
    df = load_csv(DATASET)
    if "url" not in df.columns or "label" not in df.columns:
        raise ValueError("Dataset URL phải có 2 cột: url, label")

    df = df[["url", "label"]].dropna().drop_duplicates()
    df["label"] = df["label"].map(normalize_label)

    feature_rows = [extract_url_features(url) for url in df["url"].astype(str)]
    feature_names = list(feature_rows[0].keys())
    X = [[row[name] for name in feature_names] for row in feature_rows]
    y = df["label"].tolist()

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    model = LogisticRegression(max_iter=2000, class_weight="balanced")
    model.fit(X_train, y_train)

    pred = model.predict(X_test)
    metrics = classification_metrics(y_test, pred)

    bundle = {"model": model, "feature_names": feature_names}
    save_joblib(bundle, URL_MODEL_DIR / "url_model.pkl")
    save_json(metrics, URL_MODEL_DIR / "metrics.json")

    print("URL model trained successfully.")
    print(metrics)

if __name__ == "__main__":
    main()

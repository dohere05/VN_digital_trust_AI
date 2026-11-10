from config.paths import URL_MODEL_DIR
from src.preprocessing.feature_extractor import extract_url_features
from src.services.model_service import load_joblib

MODEL_PATH = URL_MODEL_DIR / "url_model.pkl"

def predict_malicious_url(url: str) -> dict:
    features = extract_url_features(url)
    model_bundle = load_joblib(str(MODEL_PATH))

    if model_bundle is None:
        heuristic = min(
            1.0,
            features["host_is_ip"] * 0.35
            + features["suspicious_token_count"] * 0.12
            + int(features["uses_https"] == 0) * 0.10
            + int(features["url_length"] > 90) * 0.12
            + int(features["at_count"] > 0) * 0.20
            + int(features["has_punycode"] > 0) * 0.15,
        )
        return {
            "available": False,
            "label": "suspicious" if heuristic >= 0.35 else "unknown",
            "malicious_probability": heuristic,
            "features": features,
            "message": "Chưa có mô hình URL; đang dùng điểm heuristic.",
        }

    model = model_bundle["model"]
    feature_names = model_bundle["feature_names"]
    X = [[features[name] for name in feature_names]]
    prediction = model.predict(X)[0]

    probability = None
    if hasattr(model, "predict_proba"):
        classes = list(model.classes_)
        probs = model.predict_proba(X)[0]
        idx = classes.index(1) if 1 in classes else None
        if idx is not None:
            probability = float(probs[idx])

    return {
        "available": True,
        "label": "malicious" if prediction == 1 else "safe",
        "malicious_probability": probability,
        "features": features,
        "message": None,
    }

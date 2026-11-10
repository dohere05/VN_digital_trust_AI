from config.paths import SPAM_MODEL_DIR
from src.preprocessing.vietnamese_text import preprocess_vietnamese
from src.services.model_service import load_joblib

MODEL_PATH = SPAM_MODEL_DIR / "spam_model.pkl"
VECTORIZER_PATH = SPAM_MODEL_DIR / "spam_vectorizer.pkl"

def predict_spam(text: str) -> dict:
    model = load_joblib(str(MODEL_PATH))
    vectorizer = load_joblib(str(VECTORIZER_PATH))

    if model is None or vectorizer is None:
        return {
            "available": False,
            "label": None,
            "spam_probability": None,
            "message": "Chưa có mô hình Spam. Hãy chạy train/train_spam.py.",
        }

    cleaned = preprocess_vietnamese(text)
    X = vectorizer.transform([cleaned])
    prediction = model.predict(X)[0]

    spam_probability = None
    if hasattr(model, "predict_proba"):
        classes = list(model.classes_)
        probs = model.predict_proba(X)[0]
        spam_index = classes.index(1) if 1 in classes else classes.index("spam")
        spam_probability = float(probs[spam_index])

    return {
        "available": True,
        "label": "spam" if prediction in (1, "spam") else "ham",
        "spam_probability": spam_probability,
        "message": None,
    }

from config.paths import FAKE_MODEL_DIR

from src.preprocessing.vietnamese_text import (
    preprocess_vietnamese,
)

from src.services.model_service import (
    load_joblib,
)


MODEL_PATH = (
    FAKE_MODEL_DIR
    / "fake_news_model.pkl"
)

VECTORIZER_PATH = (
    FAKE_MODEL_DIR
    / "fake_news_vectorizer.pkl"
)


def predict_fake_news(
    title: str,
    content: str,
) -> dict:

    model = load_joblib(
        str(MODEL_PATH)
    )

    vectorizer = load_joblib(
        str(VECTORIZER_PATH)
    )

    if model is None or vectorizer is None:

        return {
            "available": False,
            "label": None,
            "fake_probability": None,
            "real_probability": None,
            "confidence": None,
            "message":
                "Chưa có mô hình Fake News. "
                "Hãy chạy train/train_fake_news.py.",
        }

    # =========================================
    # GHÉP TIÊU ĐỀ + NỘI DUNG
    # =========================================

    full_text = (
        f"{title} {content}"
        .strip()
    )

    processed_text = (
        preprocess_vietnamese(
            full_text
        )
    )

    # =========================================
    # VECTOR HÓA
    # =========================================

    X = vectorizer.transform(
        [processed_text]
    )

    # =========================================
    # DỰ ĐOÁN
    # =========================================

    prediction = int(
        model.predict(X)[0]
    )

    fake_probability = None
    real_probability = None

    # =========================================
    # XÁC SUẤT
    # =========================================

    if hasattr(
        model,
        "predict_proba",
    ):

        probabilities = (
            model.predict_proba(X)[0]
        )

        classes = list(
            model.classes_
        )

        if 1 in classes:

            fake_index = (
                classes.index(1)
            )

            fake_probability = float(
                probabilities[fake_index]
            )

        if 0 in classes:

            real_index = (
                classes.index(0)
            )

            real_probability = float(
                probabilities[real_index]
            )

    # =========================================
    # CONFIDENCE
    # =========================================

    confidence = None

    if prediction == 1:

        confidence = (
            fake_probability
        )

    elif prediction == 0:

        confidence = (
            real_probability
        )

    return {
        "available": True,

        "label":
            "fake"
            if prediction == 1
            else "real",

        "fake_probability":
            fake_probability,

        "real_probability":
            real_probability,

        "confidence":
            confidence,

        "processed_text":
            processed_text,

        "message":
            None,
    }
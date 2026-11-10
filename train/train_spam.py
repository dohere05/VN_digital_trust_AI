from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix,
)

from config.paths import RAW_DATA_DIR, SPAM_MODEL_DIR
from src.preprocessing.vietnamese_text import preprocess_vietnamese
from train.common.model_utils import save_joblib, save_json


TRAIN_DATASET = RAW_DATA_DIR / "spam" / "train.csv"
TEST_DATASET = RAW_DATA_DIR / "spam" / "test.csv"


def load_sms_dataset(path):
    if not path.exists():
        raise FileNotFoundError(
            f"Không tìm thấy dataset: {path}"
        )

    df = pd.read_csv(path)

    print(f"\nĐang đọc: {path.name}")
    print("Các cột:", list(df.columns))
    print("Số mẫu:", len(df))

    # Dataset chính thức dùng cột message.
    if "message" in df.columns:
        df = df.rename(columns={"message": "text"})

    if "text" not in df.columns:
        raise ValueError(
            "Dataset phải có cột 'message' hoặc 'text'."
        )

    if "label" not in df.columns:
        raise ValueError(
            "Dataset phải có cột 'label'."
        )

    df = df[["text", "label"]]
    df = df.dropna()
    df = df.drop_duplicates()

    df["text"] = df["text"].astype(str)
    df["label"] = df["label"].astype(int)

    return df


def main():
    print("=" * 60)
    print("HUẤN LUYỆN MÔ HÌNH SPAM TIẾNG VIỆT")
    print("=" * 60)

    # =========================
    # 1. LOAD DATASET
    # =========================
    train_df = load_sms_dataset(TRAIN_DATASET)
    test_df = load_sms_dataset(TEST_DATASET)

    print("\nPhân bố tập TRAIN:")
    print(train_df["label"].value_counts())

    print("\nPhân bố tập TEST:")
    print(test_df["label"].value_counts())

    # =========================
    # 2. PREPROCESSING
    # =========================
    print("\nĐang tiền xử lý dữ liệu...")

    train_df["processed_text"] = (
        train_df["text"]
        .map(preprocess_vietnamese)
    )

    test_df["processed_text"] = (
        test_df["text"]
        .map(preprocess_vietnamese)
    )

    # =========================
    # 3. TF-IDF
    # =========================
    print("Đang tạo TF-IDF...")

    vectorizer = TfidfVectorizer(
        analyzer="char_wb",
        ngram_range=(3, 5),
        min_df=2,
        max_features=70000,
        sublinear_tf=True,
    )

    X_train = vectorizer.fit_transform(
        train_df["processed_text"]
    )

    X_test = vectorizer.transform(
        test_df["processed_text"]
    )

    y_train = train_df["label"]
    y_test = test_df["label"]

    print("Số đặc trưng TF-IDF:", X_train.shape[1])

    # =========================
    # 4. TRAIN MODEL
    # =========================
    print("\nĐang huấn luyện Logistic Regression...")

    model = LogisticRegression(
        max_iter=3000,
        class_weight="balanced",
        C=4.0,
        random_state=42,
    )

    model.fit(X_train, y_train)

    # =========================
    # 5. EVALUATION
    # =========================
    y_pred = model.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(
        y_test,
        y_pred,
        zero_division=0,
    )
    recall = recall_score(
        y_test,
        y_pred,
        zero_division=0,
    )
    f1 = f1_score(
        y_test,
        y_pred,
        zero_division=0,
    )

    cm = confusion_matrix(
        y_test,
        y_pred,
    )

    print("\n" + "=" * 60)
    print("KẾT QUẢ ĐÁNH GIÁ")
    print("=" * 60)

    print(f"Accuracy : {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall   : {recall:.4f}")
    print(f"F1-score : {f1:.4f}")

    print("\nClassification Report:")
    print(
        classification_report(
            y_test,
            y_pred,
            target_names=[
                "Tin thường",
                "Spam/Lừa đảo",
            ],
            zero_division=0,
        )
    )

    print("Confusion Matrix:")
    print(cm)

    # =========================
    # 6. SAVE MODEL
    # =========================
    metrics = {
        "accuracy": float(accuracy),
        "precision": float(precision),
        "recall": float(recall),
        "f1": float(f1),
        "confusion_matrix": cm.tolist(),
        "train_samples": len(train_df),
        "test_samples": len(test_df),
        "features": X_train.shape[1],
        "model": "Logistic Regression",
        "vectorizer": "TF-IDF Char 3-5 gram",
    }

    save_joblib(
        model,
        SPAM_MODEL_DIR / "spam_model.pkl",
    )

    save_joblib(
        vectorizer,
        SPAM_MODEL_DIR / "spam_vectorizer.pkl",
    )

    save_json(
        metrics,
        SPAM_MODEL_DIR / "metrics.json",
    )

    print("\nĐã lưu:")
    print(
        SPAM_MODEL_DIR / "spam_model.pkl"
    )
    print(
        SPAM_MODEL_DIR / "spam_vectorizer.pkl"
    )
    print(
        SPAM_MODEL_DIR / "metrics.json"
    )

    print("\nHUẤN LUYỆN HOÀN TẤT!")


if __name__ == "__main__":
    main()
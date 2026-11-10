from pathlib import Path
import sys
import json

sys.path.append(str(Path(__file__).resolve().parents[1]))

import pandas as pd
import joblib

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC

from sklearn.model_selection import train_test_split

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix,
)

from config.paths import RAW_DATA_DIR, FAKE_MODEL_DIR
from src.preprocessing.vietnamese_text import preprocess_vietnamese


# ============================================================
# CẤU HÌNH
# ============================================================

RANDOM_STATE = 42
TEST_SIZE = 0.20

DATASET_PATH = (
    RAW_DATA_DIR
    / "fake_news"
    / "train.csv"
)


# ============================================================
# LOAD DATASET
# ============================================================

def load_dataset():

    if not DATASET_PATH.exists():

        raise FileNotFoundError(
            f"Không tìm thấy dataset: {DATASET_PATH}"
        )

    print("=" * 70)
    print("ĐỌC DATASET FAKE NEWS")
    print("=" * 70)

    df = pd.read_csv(DATASET_PATH)

    print(
        "\nKích thước ban đầu:",
        df.shape,
    )

    print(
        "\nCác cột:"
    )

    print(
        df.columns.tolist()
    )

    # ================================================
    # KIỂM TRA CỘT BẮT BUỘC
    # ================================================

    required_columns = {
        "post_message",
        "label",
    }

    if not required_columns.issubset(
        df.columns
    ):

        raise ValueError(
            "Dataset cần có hai cột: "
            "'post_message' và 'label'."
        )

    # ================================================
    # CHỈ GIỮ DATA CẦN THIẾT
    # ================================================

    df = df[
        [
            "post_message",
            "label",
        ]
    ].copy()

    # ================================================
    # DROP NULL
    # ================================================

    before_null = len(df)

    df = df.dropna(
        subset=[
            "post_message",
            "label",
        ]
    )

    print(
        "\nSố mẫu null đã loại:",
        before_null - len(df),
    )

    # ================================================
    # CHUYỂN KIỂU
    # ================================================

    df["post_message"] = (
        df["post_message"]
        .astype(str)
        .str.strip()
    )

    df["label"] = (
        df["label"]
        .astype(int)
    )

    # ================================================
    # CHỈ GIỮ NHÃN 0 / 1
    # ================================================

    df = df[
        df["label"].isin(
            [0, 1]
        )
    ].copy()

    # ================================================
    # LOẠI NỘI DUNG QUÁ NGẮN
    # ================================================

    df["text_length"] = (
        df["post_message"]
        .str.len()
    )

    before_short = len(df)

    df = df[
        df["text_length"] >= 20
    ].copy()

    print(
        "Số mẫu quá ngắn đã loại:",
        before_short - len(df),
    )

    # ================================================
    # LOẠI DUPLICATE
    # ================================================

    before_duplicate = len(df)

    df = df.drop_duplicates(
        subset=[
            "post_message"
        ]
    )

    print(
        "Số duplicate đã loại:",
        before_duplicate - len(df),
    )

    # ================================================
    # THỐNG KÊ
    # ================================================

    print(
        "\nSố mẫu cuối cùng:",
        len(df),
    )

    print(
        "\nPhân bố nhãn:"
    )

    print(
        df["label"]
        .value_counts()
        .sort_index()
    )

    print(
        "\nTỷ lệ nhãn:"
    )

    distribution = (
        df["label"]
        .value_counts(
            normalize=True
        )
        .sort_index()
        * 100
    )

    print(
        distribution.round(2)
    )

    return df


# ============================================================
# PREPROCESS
# ============================================================

def preprocess_dataset(
    df,
):

    print(
        "\nĐang tiền xử lý tiếng Việt..."
    )

    df = df.copy()

    df["processed_text"] = (
        df["post_message"]
        .map(
            preprocess_vietnamese
        )
    )

    # ================================================
    # LOẠI TEXT RỖNG SAU PREPROCESS
    # ================================================

    df = df[
        df["processed_text"]
        .str.strip()
        .str.len()
        > 0
    ].copy()

    return df


# ============================================================
# ĐÁNH GIÁ MODEL
# ============================================================

def evaluate_model(
    model_name,
    model,
    X_test,
    y_test,
):

    predictions = (
        model.predict(
            X_test
        )
    )

    accuracy = accuracy_score(
        y_test,
        predictions,
    )

    precision = precision_score(
        y_test,
        predictions,
        pos_label=1,
        zero_division=0,
    )

    recall = recall_score(
        y_test,
        predictions,
        pos_label=1,
        zero_division=0,
    )

    f1 = f1_score(
        y_test,
        predictions,
        pos_label=1,
        zero_division=0,
    )

    cm = confusion_matrix(
        y_test,
        predictions,
        labels=[0, 1],
    )

    print(
        "\n"
        + "=" * 70
    )

    print(
        f"KẾT QUẢ MODEL: {model_name}"
    )

    print(
        "=" * 70
    )

    print(
        f"Accuracy : {accuracy:.4f}"
    )

    print(
        f"Precision: {precision:.4f}"
    )

    print(
        f"Recall   : {recall:.4f}"
    )

    print(
        f"F1-score : {f1:.4f}"
    )

    print(
        "\nClassification Report:"
    )

    print(
        classification_report(
            y_test,
            predictions,
            labels=[0, 1],
            target_names=[
                "Tin thật",
                "Tin giả",
            ],
            zero_division=0,
        )
    )

    print(
        "Confusion Matrix:"
    )

    print(
        cm
    )

    return {

        "model_name":
            model_name,

        "accuracy":
            float(accuracy),

        "precision":
            float(precision),

        "recall":
            float(recall),

        "f1":
            float(f1),

        "confusion_matrix":
            cm.tolist(),
    }


# ============================================================
# MAIN
# ============================================================

def main():

    print(
        "\n"
        + "=" * 70
    )

    print(
        "HUẤN LUYỆN MÔ HÌNH FAKE NEWS TIẾNG VIỆT"
    )

    print(
        "=" * 70
    )

    # ========================================================
    # 1. LOAD DATA
    # ========================================================

    df = load_dataset()

    # ========================================================
    # 2. PREPROCESS
    # ========================================================

    df = preprocess_dataset(
        df
    )

    # ========================================================
    # 3. TRAIN / TEST SPLIT
    # ========================================================

    X_train_text, X_test_text, y_train, y_test = (
        train_test_split(

            df["processed_text"],

            df["label"],

            test_size=TEST_SIZE,

            random_state=RANDOM_STATE,

            stratify=df["label"],
        )
    )

    print(
        "\nTrain samples:",
        len(X_train_text),
    )

    print(
        "Test samples:",
        len(X_test_text),
    )

    print(
        "\nPhân bố TRAIN:"
    )

    print(
        y_train
        .value_counts()
        .sort_index()
    )

    print(
        "\nPhân bố TEST:"
    )

    print(
        y_test
        .value_counts()
        .sort_index()
    )

    # ========================================================
    # 4. TF-IDF WORD N-GRAM
    # ========================================================

    print(
        "\nĐang xây dựng TF-IDF..."
    )

    vectorizer = TfidfVectorizer(

        analyzer="word",

        ngram_range=(1, 2),

        min_df=2,

        max_df=0.98,

        max_features=100000,

        sublinear_tf=True,

        lowercase=False,
    )

    X_train = (
        vectorizer
        .fit_transform(
            X_train_text
        )
    )

    X_test = (
        vectorizer
        .transform(
            X_test_text
        )
    )

    print(
        "Số đặc trưng TF-IDF:",
        X_train.shape[1],
    )

    # ========================================================
    # 5. CÁC MODEL
    # ========================================================

    models = {

        "Logistic Regression":
            LogisticRegression(

                max_iter=3000,

                class_weight="balanced",

                C=3.0,

                random_state=RANDOM_STATE,
            ),

        "Linear SVM":
            LinearSVC(

                C=1.5,

                class_weight="balanced",

                random_state=RANDOM_STATE,
            ),

        "Multinomial Naive Bayes":
            MultinomialNB(

                alpha=0.35,
            ),
    }

    results = {}

    trained_models = {}

    # ========================================================
    # 6. TRAIN
    # ========================================================

    for (
        model_name,
        model,
    ) in models.items():

        print(
            "\nĐang huấn luyện:",
            model_name,
        )

        model.fit(
            X_train,
            y_train,
        )

        metrics = evaluate_model(

            model_name,

            model,

            X_test,

            y_test,
        )

        results[
            model_name
        ] = metrics

        trained_models[
            model_name
        ] = model

    # ========================================================
    # 7. CHỌN MODEL TỐT NHẤT THEO F1 CỦA TIN GIẢ
    # ========================================================

    best_model_name = max(

        results,

        key=lambda name:
            results[name]["f1"],
    )

    best_model = (
        trained_models[
            best_model_name
        ]
    )

    best_metrics = (
        results[
            best_model_name
        ]
    )

    print(
        "\n"
        + "=" * 70
    )

    print(
        "MODEL TỐT NHẤT"
    )

    print(
        "=" * 70
    )

    print(
        "Model:",
        best_model_name,
    )

    print(
        "F1 Fake:",
        f"{best_metrics['f1']:.4f}",
    )

    print(
        "Recall Fake:",
        f"{best_metrics['recall']:.4f}",
    )

    print(
        "Precision Fake:",
        f"{best_metrics['precision']:.4f}",
    )

    print(
        "Accuracy:",
        f"{best_metrics['accuracy']:.4f}",
    )

    # ========================================================
    # 8. SAVE MODEL
    # ========================================================

    FAKE_MODEL_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    # --------------------------------------------------------
    # Lưu model tốt nhất để báo cáo
    # --------------------------------------------------------

    joblib.dump(

        best_model,

        FAKE_MODEL_DIR
        / "best_fake_news_model.pkl",
    )

    # --------------------------------------------------------
    # UI dùng Logistic Regression
    # vì có predict_proba()
    # --------------------------------------------------------

    logistic_model = (
        trained_models[
            "Logistic Regression"
        ]
    )

    joblib.dump(

        logistic_model,

        FAKE_MODEL_DIR
        / "fake_news_model.pkl",
    )

    # --------------------------------------------------------
    # Vectorizer
    # --------------------------------------------------------

    joblib.dump(

        vectorizer,

        FAKE_MODEL_DIR
        / "fake_news_vectorizer.pkl",
    )

    # ========================================================
    # 9. SAVE METRICS
    # ========================================================

    metrics_data = {

        "dataset":
            "train.csv",

        "original_samples":
            5172,

        "final_samples":
            len(df),

        "train_samples":
            len(X_train_text),

        "test_samples":
            len(X_test_text),

        "features":
            X_train.shape[1],

        "label_mapping": {

            "0":
                "real",

            "1":
                "fake",
        },

        "best_model":
            best_model_name,

        "best_model_metrics":
            best_metrics,

        "all_models":
            results,

        "ui_model":
            "Logistic Regression",

        "vectorizer":
            "TF-IDF Word Unigram + Bigram",
    }

    metrics_path = (
        FAKE_MODEL_DIR
        / "metrics.json"
    )

    metrics_path.write_text(

        json.dumps(

            metrics_data,

            ensure_ascii=False,

            indent=2,
        ),

        encoding="utf-8",
    )

    # ========================================================
    # DONE
    # ========================================================

    print(
        "\nĐã lưu:"
    )

    print(
        FAKE_MODEL_DIR
        / "fake_news_model.pkl"
    )

    print(
        FAKE_MODEL_DIR
        / "best_fake_news_model.pkl"
    )

    print(
        FAKE_MODEL_DIR
        / "fake_news_vectorizer.pkl"
    )

    print(
        FAKE_MODEL_DIR
        / "metrics.json"
    )

    print(
        "\nHUẤN LUYỆN FAKE NEWS HOÀN TẤT!"
    )


if __name__ == "__main__":

    main()
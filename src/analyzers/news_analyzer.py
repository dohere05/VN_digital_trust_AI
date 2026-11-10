from src.detectors.fake_news_detector import (
    predict_fake_news,
)

from src.detectors.fake_news_signal_detector import (
    detect_fake_news_signals,
)


def analyze_news(
    title: str,
    content: str,
) -> dict:

    # =====================================
    # AI MODEL
    # =====================================

    prediction = predict_fake_news(
        title,
        content,
    )

    # =====================================
    # RULE / SIGNAL ANALYSIS
    # =====================================

    signals = detect_fake_news_signals(
        title,
        content,
    )

    fake_probability = (
        prediction.get(
            "fake_probability"
        )
    )

    # =====================================
    # RISK LEVEL
    # =====================================

    if fake_probability is None:

        level = "unknown"

    elif fake_probability >= 0.75:

        level = "high"

    elif fake_probability >= 0.45:

        level = "medium"

    else:

        level = "low"

    # =====================================
    # TEXT STATISTICS
    # =====================================

    full_text = (
        f"{title} {content}"
        .strip()
    )

    word_count = len(
        full_text.split()
    )

    char_count = len(
        full_text
    )

    return {
        "prediction":
            prediction,

        "signals":
            signals,

        "risk_level":
            level,

        "statistics": {
            "characters":
                char_count,

            "words":
                word_count,
        },
    }
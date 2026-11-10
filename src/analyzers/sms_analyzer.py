from src.detectors.spam_detector import predict_spam
from src.detectors.scam_signal_detector import (
    detect_scam_signals,
)
from src.analyzers.url_analyzer import analyze_url
from src.validators.hotline_validator import (
    validate_hotline,
)
from src.risk_engine.risk_engine import (
    calculate_sms_risk,
)


def analyze_sms(
    text: str,
    sender: str = "",
) -> dict:

    # ===============================
    # AI SPAM
    # ===============================

    spam = predict_spam(
        text
    )

    # ===============================
    # SCAM SIGNALS
    # ===============================

    scam = detect_scam_signals(
        text
    )

    # ===============================
    # SENDER / HOTLINE
    # ===============================

    sender_result = validate_hotline(
        sender
    )

    # ===============================
    # URL TRONG SMS
    # ===============================

    url_results = []

    for url in scam["urls"]:

        url_result = analyze_url(
            url
        )

        url_results.append(
            url_result
        )

    if url_results:

        url_risk = max(
            item["risk"]["score"]
            for item in url_results
        )

    else:

        url_risk = None

    # ===============================
    # SENDER TRUST
    # ===============================

    if sender_result["provided"]:

        sender_verified = (
            sender_result["verified"]
        )

    else:

        sender_verified = None

    # ===============================
    # RISK ENGINE
    # ===============================

    risk = calculate_sms_risk(
        spam.get(
            "spam_probability"
        ),
        scam["score"],
        url_risk,
        sender_verified,
    )

    # ===============================
    # KẾT QUẢ
    # ===============================

    return {

        "spam": spam,

        "scam": scam,

        "sender":
            sender_result,

        "urls":
            url_results,

        "risk":
            risk,
    }
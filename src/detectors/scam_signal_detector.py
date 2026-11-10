import json
import re

from config.paths import SUSPICIOUS_KEYWORDS_FILE
from src.utils.helpers import extract_urls


MONEY_PATTERNS = [
    r"\b\d{1,3}(?:[.,]\d{3})+(?:\s*)(?:vnd|đ|vnđ|dong|đồng)?\b",
    r"\b\d+(?:\s*)(?:triệu|trieu|tỷ|ty)\b",
]


PHONE_PATTERN = re.compile(
    r"(?<!\d)(?:\+?84|0)\d{8,10}(?!\d)"
)


def _load_rules():
    try:
        with open(
            SUSPICIOUS_KEYWORDS_FILE,
            "r",
            encoding="utf-8",
        ) as file:
            return json.load(file)

    except Exception:
        return {}


def _detect_money(text):
    results = []

    for pattern in MONEY_PATTERNS:
        matches = re.findall(
            pattern,
            text,
            flags=re.IGNORECASE,
        )

        results.extend(matches)

    return list(dict.fromkeys(results))


def detect_scam_signals(text: str) -> dict:

    original_text = text or ""
    text_lower = original_text.lower()

    rules = _load_rules()

    signals = []
    total_score = 0.0

    # ==========================================
    # PHÂN TÍCH KEYWORD THEO NHÓM
    # ==========================================

    for rule_id, rule in rules.items():

        keywords = rule.get(
            "keywords",
            [],
        )

        hits = []

        for keyword in keywords:

            if keyword.lower() in text_lower:
                hits.append(keyword)

        if hits:

            weight = float(
                rule.get(
                    "weight",
                    0.1,
                )
            )

            total_score += weight

            signals.append(
                {
                    "id": rule_id,
                    "title": rule.get(
                        "title",
                        rule_id,
                    ),
                    "severity": rule.get(
                        "severity",
                        "medium",
                    ),
                    "weight": weight,
                    "matches": hits,
                }
            )

    # ==========================================
    # PHÁT HIỆN SỐ TIỀN
    # ==========================================

    money_matches = _detect_money(
        original_text
    )

    if money_matches:

        total_score += 0.18

        signals.append(
            {
                "id": "money_amount",
                "title":
                    "Có đề cập số tiền / giá trị tài chính",
                "severity": "high",
                "weight": 0.18,
                "matches": money_matches,
            }
        )

    # ==========================================
    # URL
    # ==========================================

    urls = extract_urls(
        original_text
    )

    if urls:

        total_score += 0.15

        signals.append(
            {
                "id": "url",
                "title":
                    "Tin nhắn chứa đường dẫn",
                "severity": "medium",
                "weight": 0.15,
                "matches": urls,
            }
        )

    # ==========================================
    # SĐT TRONG NỘI DUNG
    # ==========================================

    phones = PHONE_PATTERN.findall(
        original_text
    )

    if phones:

        signals.append(
            {
                "id": "phone_number",
                "title":
                    "Phát hiện số điện thoại trong nội dung",
                "severity": "low",
                "weight": 0.02,
                "matches": phones,
            }
        )

    # ==========================================
    # KÝ TỰ ! BẤT THƯỜNG
    # ==========================================

    exclamation_count = original_text.count(
        "!"
    )

    if exclamation_count >= 3:

        total_score += 0.05

        signals.append(
            {
                "id": "excessive_exclamation",
                "title":
                    "Sử dụng nhiều dấu chấm than",
                "severity": "low",
                "weight": 0.05,
                "matches": [
                    f"{exclamation_count} dấu !"
                ],
            }
        )

    # ==========================================
    # GIỚI HẠN SCORE
    # ==========================================

    total_score = min(
        1.0,
        total_score,
    )

    severity_order = {
        "high": 0,
        "medium": 1,
        "low": 2,
    }

    signals.sort(
        key=lambda item:
            severity_order.get(
                item["severity"],
                3,
            )
    )

    return {
        "score": total_score,
        "signals": signals,
        "urls": urls,
        "phones": phones,
        "money": money_matches,
        "signal_count": len(signals),
    }
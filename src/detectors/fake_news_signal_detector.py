import re


RULES = {

    "unverified_source": {
        "title":
            "Nguồn thông tin chưa được xác minh",

        "severity":
            "high",

        "keywords": [
            "chưa được xác minh",
            "chưa kiểm chứng",
            "chưa được kiểm chứng",
            "nguồn tin chưa được xác nhận",
            "nguồn tin bí mật",
            "nguồn tin nội bộ",
            "nguồn tin không chính thức",
            "nghe nói rằng",
            "có thông tin cho rằng",
        ],
    },

    "sensational": {
        "title":
            "Ngôn ngữ giật gân / gây sốc",

        "severity":
            "medium",

        "keywords": [
            "gây sốc",
            "chấn động",
            "kinh hoàng",
            "không thể tin nổi",
            "bí mật động trời",
            "sự thật gây sốc",
            "cả thế giới sửng sốt",
            "ai cũng phải biết",
            "không ai ngờ",
        ],
    },

    "urgency": {
        "title":
            "Kêu gọi chia sẻ hoặc hành động gấp",

        "severity":
            "medium",

        "keywords": [
            "chia sẻ ngay",
            "hãy chia sẻ",
            "hãy chia sẻ ngay",
            "lan truyền ngay",
            "đừng để bị xóa",
            "trước khi bị xóa",
            "hãy đọc ngay",
            "cảnh báo khẩn cấp",
        ],
    },

    "absolute_claim": {
        "title":
            "Khẳng định tuyệt đối",

        "severity":
            "medium",

        "keywords": [
            "100% sự thật",
            "100% chính xác",
            "chắc chắn đúng",
            "không thể sai",
            "hoàn toàn đúng",
            "cam kết đúng",
        ],
    },

    "conspiracy": {
        "title":
            "Ngôn ngữ mang tính âm mưu / che giấu",

        "severity":
            "medium",

        "keywords": [
            "bị che giấu",
            "cố tình che giấu",
            "truyền thông không nói",
            "báo chí không dám đăng",
            "sự thật bị che giấu",
            "âm mưu",
        ],
    },

    "anonymous_authority": {
        "title":
            "Dẫn nguồn mơ hồ",

        "severity":
            "medium",

        "keywords": [
            "các chuyên gia cho biết",
            "một chuyên gia cho biết",
            "nhiều người cho rằng",
            "theo một nguồn tin",
            "theo người trong cuộc",
            "theo cộng đồng mạng",
        ],
    },
}


def detect_fake_news_signals(
    title: str,
    content: str,
) -> dict:

    original_text = (
        f"{title} {content}"
    )

    text_lower = (
        original_text.lower()
    )

    signals = []

    # =====================================
    # KEYWORD RULES
    # =====================================

    for rule_id, rule in RULES.items():

        matches = []

        for keyword in rule["keywords"]:

            if keyword in text_lower:

                matches.append(
                    keyword
                )

        if matches:

            signals.append({
                "id":
                    rule_id,

                "title":
                    rule["title"],

                "severity":
                    rule["severity"],

                "matches":
                    matches,
            })

    # =====================================
    # NHIỀU DẤU CHẤM THAN
    # =====================================

    exclamation_count = (
        original_text.count("!")
    )

    if exclamation_count >= 3:

        signals.append({
            "id":
                "exclamation",

            "title":
                "Sử dụng nhiều dấu chấm than",

            "severity":
                "low",

            "matches": [
                f"{exclamation_count} dấu !"
            ],
        })

    # =====================================
    # NHIỀU DẤU HỎI
    # =====================================

    question_count = (
        original_text.count("?")
    )

    if question_count >= 4:

        signals.append({
            "id":
                "question",

            "title":
                "Sử dụng nhiều câu hỏi gây nghi vấn",

            "severity":
                "low",

            "matches": [
                f"{question_count} dấu ?"
            ],
        })

    # =====================================
    # VIẾT HOA
    # =====================================

    uppercase_words = re.findall(
        r"\b[A-ZÀ-Ỹ]{4,}\b",
        original_text,
    )

    uppercase_words = list(
        dict.fromkeys(
            uppercase_words
        )
    )

    if len(uppercase_words) >= 3:

        signals.append({
            "id":
                "uppercase",

            "title":
                "Có nhiều từ viết hoa",

            "severity":
                "low",

            "matches":
                uppercase_words[:10],
        })

    return {
        "signals":
            signals,

        "signal_count":
            len(signals),

        "exclamation_count":
            exclamation_count,

        "question_count":
            question_count,

        "uppercase_words":
            uppercase_words,
    }
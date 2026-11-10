"""Lưu và đọc lịch sử kiểm tra cục bộ của ứng dụng."""

from __future__ import annotations

import json
from datetime import datetime
from typing import Any

import streamlit as st


HISTORY_SESSION_KEY = "vdt_history"
HISTORY_NEXT_ID_KEY = "vdt_history_next_id"


CHECK_TYPE_LABELS = {
    "news": "Tin tức",
    "sms": "Tin nhắn",
    "email": "Email",
    "phone": "Số điện thoại / Hotline",
    "url": "URL",
}

RISK_LABELS = {
    "low": "Rủi ro thấp",
    "medium": "Cần thận trọng",
    "high": "Nguy cơ cao",
    "unknown": "Chưa đủ dữ liệu",
}


def initialize_history_session() -> None:
    """Tạo vùng lịch sử chỉ tồn tại trong phiên Streamlit hiện tại."""
    if HISTORY_SESSION_KEY not in st.session_state:
        st.session_state[HISTORY_SESSION_KEY] = []
    if HISTORY_NEXT_ID_KEY not in st.session_state:
        st.session_state[HISTORY_NEXT_ID_KEY] = 1


def _risk_from_result(check_type: str, result: dict[str, Any]) -> tuple[str, float | None]:
    if check_type == "news":
        prediction = result.get("prediction", {})
        return result.get("risk_level", "unknown"), prediction.get("fake_probability")

    risk = result.get("risk", {})
    return risk.get("level", "unknown"), risk.get("score")


def _yes_no(value: bool, yes: str = "Có", no: str = "Không") -> str:
    return yes if value else no


def build_report(check_type: str, result: dict[str, Any]) -> str:
    """Chuyển kết quả kỹ thuật thành báo cáo ngắn, dễ đọc trong lịch sử."""
    risk_level, risk_score = _risk_from_result(check_type, result)
    risk_text = RISK_LABELS.get(risk_level, RISK_LABELS["unknown"])
    score_text = f" ({risk_score * 100:.1f}/100)" if risk_score is not None else ""
    lines = [f"Đánh giá tổng quan: {risk_text}{score_text}."]

    if check_type == "news":
        prediction = result.get("prediction", {})
        if not prediction.get("available"):
            lines.append(prediction.get("message", "Mô hình AI hiện chưa sẵn sàng."))
        else:
            label = "có dấu hiệu tin giả" if prediction.get("label") == "fake" else "có dấu hiệu tin thật"
            lines.append(f"AI đánh giá nội dung {label}.")
            fake_probability = prediction.get("fake_probability")
            if fake_probability is not None:
                lines.append(f"Khả năng tin giả: {fake_probability * 100:.1f}%.")
            lines.append(
                f"Đã phát hiện {result.get('signals', {}).get('signal_count', 0)} dấu hiệu cần chú ý."
            )

    elif check_type == "sms":
        spam = result.get("spam", {})
        if spam.get("available"):
            label = "có dấu hiệu spam/lừa đảo" if spam.get("label") == "spam" else "gần với tin nhắn thông thường"
            lines.append(f"AI đánh giá tin nhắn {label}.")
            if spam.get("spam_probability") is not None:
                lines.append(f"Khả năng spam: {spam['spam_probability'] * 100:.1f}%.")
        else:
            lines.append(spam.get("message", "Mô hình AI hiện chưa sẵn sàng."))
        lines.append(f"Đã phát hiện {result.get('scam', {}).get('signal_count', 0)} dấu hiệu lừa đảo.")

    elif check_type == "email":
        email = result.get("email", {})
        lines.append(f"Định dạng email: {_yes_no(email.get('valid_format', False), 'hợp lệ', 'không hợp lệ')}.")
        if email.get("valid_format"):
            domain = result.get("domain", {})
            lines.append(f"DNS: {_yes_no(domain.get('dns_exists', False))}; MX: {_yes_no(bool(domain.get('mx_records')))}.")
            lines.append(f"Email tạm thời: {_yes_no(result.get('disposable', False))}.")
        elif email.get("error"):
            lines.append(email["error"])

    elif check_type == "phone":
        phone = result.get("phone", {})
        lines.append(f"Số điện thoại hợp lệ: {_yes_no(phone.get('valid', False))}.")
        hotline = result.get("hotline", {})
        if hotline.get("provided"):
            verified = _yes_no(hotline.get("verified", False), "đã xác minh", "chưa xác minh")
            lines.append(f"Hotline: {verified}.")

    elif check_type == "url":
        validation = result.get("validation", {})
        detection = result.get("detection", {})
        lines.append(f"Cú pháp URL: {_yes_no(validation.get('valid_syntax', False), 'hợp lệ', 'không hợp lệ')}.")
        lines.append(f"DNS: {_yes_no(validation.get('dns_exists', False))}; HTTPS: {_yes_no(validation.get('https', False))}.")
        probability = detection.get("malicious_probability")
        if probability is not None:
            lines.append(f"Điểm nghi ngờ URL: {probability * 100:.1f}%.")
        elif detection.get("message"):
            lines.append(detection["message"])

    return "\n\n".join(lines)


def record_check(check_type: str, input_data: dict[str, Any], result: dict[str, Any]) -> int:
    """Ghi kết quả ngay vào lịch sử của phiên web hiện tại."""
    if check_type not in CHECK_TYPE_LABELS:
        raise ValueError(f"Loại kiểm tra không hợp lệ: {check_type}")

    initialize_history_session()
    risk_level, risk_score = _risk_from_result(check_type, result)
    history_id = st.session_state[HISTORY_NEXT_ID_KEY]
    st.session_state[HISTORY_NEXT_ID_KEY] = history_id + 1

    # JSON tạo bản sao của kết quả tại thời điểm phân tích, không bị thay đổi
    # nếu các biến của giao diện được cập nhật ở lần chạy sau.
    input_snapshot = json.loads(json.dumps(input_data, ensure_ascii=False, default=str))
    result_snapshot = json.loads(json.dumps(result, ensure_ascii=False, default=str))
    record = {
        "id": history_id,
        "check_type": check_type,
        "input_data": input_snapshot,
        "report_text": build_report(check_type, result_snapshot),
        "result_data": result_snapshot,
        "risk_level": risk_level,
        "risk_score": risk_score,
        "created_at": datetime.now().astimezone().strftime("%d/%m/%Y %H:%M:%S"),
    }
    st.session_state[HISTORY_SESSION_KEY].insert(0, record)
    return history_id


def get_history(limit: int = 100) -> list[dict[str, Any]]:
    """Lấy các lần kiểm tra gần nhất của riêng phiên web đang mở."""
    initialize_history_session()
    return st.session_state[HISTORY_SESSION_KEY][:limit]

import streamlit as st

from src.analyzers.url_analyzer import analyze_url
from src.services.history_service import record_check
from ui.components.confidence_bar import render_confidence
from ui.components.risk_badge import render_risk_badge


def _render_result(result: dict) -> None:
    st.divider()
    render_risk_badge(result["risk"]["level"], result["risk"]["score"])

    validation = result["validation"]
    detection = result["detection"]
    st.write("**URL chuẩn hóa:**", validation["normalized"])
    st.write("**Cú pháp:**", "✅ Hợp lệ" if validation["valid_syntax"] else "❌ Không hợp lệ")
    st.write("**Domain:**", validation["domain"] or "Không xác định")
    st.write("**DNS:**", "✅ Tồn tại" if validation["dns_exists"] else "❌ Không xác nhận được")
    st.write("**HTTPS:**", "✅ Có" if validation["https"] else "⚠️ Không")
    render_confidence(detection.get("malicious_probability"), "Điểm nghi ngờ URL")

    if detection.get("message"):
        st.info(detection["message"])

    with st.expander("Đặc trưng kỹ thuật"):
        st.json(detection["features"])


def render() -> None:
    st.subheader("🔗 Kiểm tra URL")
    st.caption("Phân tích cú pháp, DNS, HTTPS và dấu hiệu URL độc hại.")

    url = st.text_input("URL *", placeholder="https://example.com")
    analyze_clicked = st.button("Phân tích URL", type="primary", use_container_width=True)

    if analyze_clicked:
        if not url.strip():
            st.warning("Vui lòng nhập URL.")
            return

        result = analyze_url(url)
        record_check("url", {"URL": url}, result)
        st.session_state["last_url_result"] = result
        st.toast("Đã lưu kết quả vào lịch sử phiên này.", icon="🕘")

    result = st.session_state.get("last_url_result")
    if result is not None:
        _render_result(result)

import streamlit as st

from src.analyzers.email_analyzer import analyze_email
from src.services.history_service import record_check
from ui.components.risk_badge import render_risk_badge


def _render_result(result: dict) -> None:
    st.divider()
    render_risk_badge(result["risk"]["level"], result["risk"]["score"])

    base = result["email"]
    st.write("**Định dạng:**", "✅ Hợp lệ" if base["valid_format"] else "❌ Không hợp lệ")
    if not base["valid_format"]:
        st.caption(base["error"])
        return

    st.write("**Email chuẩn hóa:**", base["normalized"])
    st.write("**Domain:**", base["domain"])
    st.write("**DNS:**", "✅ Tồn tại" if result["domain"]["dns_exists"] else "❌ Không xác nhận được")
    st.write("**Mail server (MX):**", "✅ Có" if result["domain"]["mx_records"] else "❌ Không tìm thấy")
    st.write("**Email tạm:**", "⚠️ Có dấu hiệu" if result["disposable"] else "✅ Không nằm trong danh sách hiện tại")
    st.caption("Hệ thống không xác nhận hộp thư có người sử dụng thật hay thuộc về ai.")


def render() -> None:
    st.subheader("✉️ Kiểm tra Email")
    st.caption("Kiểm tra cú pháp, domain, MX và dấu hiệu email tạm.")

    email = st.text_input("Địa chỉ Email *", placeholder="example@domain.com")
    check_clicked = st.button("Kiểm tra Email", type="primary", use_container_width=True)

    if check_clicked:
        if not email.strip():
            st.warning("Vui lòng nhập email.")
            return

        result = analyze_email(email)
        record_check("email", {"Địa chỉ email": email}, result)
        st.session_state["last_email_result"] = result
        st.toast("Đã lưu kết quả vào lịch sử phiên này.", icon="🕘")

    result = st.session_state.get("last_email_result")
    if result is not None:
        _render_result(result)

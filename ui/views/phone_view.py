import streamlit as st

from src.analyzers.phone_analyzer import analyze_phone
from src.services.history_service import record_check
from ui.components.risk_badge import render_risk_badge


def _render_result(result: dict) -> None:
    st.divider()
    render_risk_badge(result["risk"]["level"], result["risk"]["score"])

    phone = result["phone"]
    st.write("**Số hợp lệ:**", "✅ Có" if phone["valid"] else "❌ Không")
    st.write("**Số có thể tồn tại theo cấu trúc:**", "✅ Có" if phone["possible"] else "❌ Không")

    if phone["international"]:
        st.write("**Chuẩn quốc tế:**", phone["international"])
        st.write("**Loại:**", phone["type"] or "Không xác định")
        st.write("**Nhà mạng:**", phone["carrier"] or "Không xác định")
        st.write("**Khu vực:**", phone["location"] or "Không xác định")

    hotline = result["hotline"]
    if hotline["provided"]:
        if hotline["verified"]:
            st.success(f"Hotline đã xác minh: {hotline.get('organization') or 'Không rõ tổ chức'}")
        else:
            st.info("Số này không nằm trong danh sách hotline đã xác minh của hệ thống.")

    st.caption("Chỉ từ số điện thoại không thể khẳng định chắc chắn đây là SIM ảo, số giả hay danh tính của người sử dụng.")


def render() -> None:
    st.subheader("📱 Kiểm tra số điện thoại / Hotline")
    st.caption("Mặc định phân tích số Việt Nam nếu không có mã quốc gia.")

    phone = st.text_input("Số điện thoại *", placeholder="Ví dụ: 0912345678 hoặc +84912345678")
    check_clicked = st.button("Kiểm tra SĐT", type="primary", use_container_width=True)

    if check_clicked:
        if not phone.strip():
            st.warning("Vui lòng nhập số điện thoại.")
            return

        result = analyze_phone(phone)
        record_check("phone", {"Số điện thoại": phone}, result)
        st.session_state["last_phone_result"] = result
        st.toast(" kết quả vào lịch sử phiên này.", icon="🕘")

    result = st.session_state.get("last_phone_result")
    if result is not None:
        _render_result(result)

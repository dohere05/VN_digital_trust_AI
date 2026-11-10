"""Giao diện xem lại lịch sử kiểm tra trong một hộp thoại trung tâm."""

from __future__ import annotations

import streamlit as st

from src.services.history_service import CHECK_TYPE_LABELS, RISK_LABELS, get_history


@st.dialog("🕘 Lịch sử kiểm tra")
def show_history_dialog() -> None:
    """Hiển thị lần kiểm tra mới nhất trước để người dùng xem lại."""
    records = get_history()

    if not records:
        st.info("Chưa có lần kiểm tra nào. Kết quả của bạn sẽ xuất hiện tại đây sau khi phân tích.")
        return

    st.caption(
        "Lịch sử chỉ được giữ trong phiên web hiện tại và sẽ tự xóa khi bạn đóng trang. "
        "Hiển thị tối đa 100 lần kiểm tra gần nhất."
    )

    for record in records:
        check_name = CHECK_TYPE_LABELS.get(record["check_type"], record["check_type"])
        risk_name = RISK_LABELS.get(record["risk_level"], RISK_LABELS["unknown"])
        score = record.get("risk_score")
        score_text = f" · {score * 100:.1f}/100" if score is not None else ""
        label = f"{record['created_at']} · {check_name} · {risk_name}{score_text}"

        with st.expander(label):
            st.markdown("#### Thông tin đã kiểm tra")
            for name, value in record["input_data"].items():
                if value not in (None, ""):
                    st.markdown(f"**{name}:**")
                    st.code(str(value), language=None)

            st.markdown("#### Báo cáo AI")
            st.markdown(record["report_text"])

            with st.expander("Xem dữ liệu phân tích chi tiết"):
                st.json(record["result_data"], expanded=True)


def render_history_button() -> None:
    """Đặt biểu tượng lịch sử ở phía trên bên phải của ứng dụng."""
    spacer, action = st.columns([11, 1])
    with action:
        if st.button("🕘", key="history_button", help="Xem lịch sử kiểm tra"):
            show_history_dialog()

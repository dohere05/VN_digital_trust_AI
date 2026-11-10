import streamlit as st

def render_confidence(value: float | None, label: str = "Độ tin cậy"):
    if value is None:
        st.caption(f"{label}: chưa có dữ liệu xác suất.")
        return
    value = max(0.0, min(1.0, float(value)))
    st.write(f"**{label}: {value * 100:.1f}%**")
    st.progress(value)

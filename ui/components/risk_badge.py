import streamlit as st

def render_risk_badge(level: str, score: float | None = None):
    labels = {
        "low": "✅ RỦI RO THẤP",
        "medium": "⚠️ CẦN THẬN TRỌNG",
        "high": "🚨 NGUY CƠ CAO",
        "unknown": "ℹ️ CHƯA ĐỦ DỮ LIỆU",
    }
    st.subheader(labels.get(level, labels["unknown"]))
    if score is not None:
        st.caption(f"Điểm rủi ro tổng hợp: {score * 100:.1f}/100")

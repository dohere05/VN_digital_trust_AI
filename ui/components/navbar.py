import streamlit as st

NAV_ITEMS = ["📰 Tin tức", "💬 Tin nhắn", "✉️ Email", "📱 SĐT", "🔗 URL"]

def render_navbar() -> str:
    return st.radio(
        "Chức năng",
        NAV_ITEMS,
        horizontal=True,
        label_visibility="collapsed",
        key="main_nav",
    )

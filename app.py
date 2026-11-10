from pathlib import Path
import streamlit as st

from config.settings import APP_NAME
from ui.components.header import render_header
from ui.components.navbar import render_navbar
from ui.components.footer import render_footer
from ui.views import fake_news_view, spam_view, email_view, phone_view, url_view, history_view

st.set_page_config(
    page_title=APP_NAME,
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

css_path = Path("assets/styles/custom.css")
if css_path.exists():
    st.markdown(f"<style>{css_path.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)

history_view.render_history_button()
render_header()
page = render_navbar()
st.divider()

if page == "📰 Tin tức":
    fake_news_view.render()
elif page == "💬 Tin nhắn":
    spam_view.render()
elif page == "✉️ Email":
    email_view.render()
elif page == "📱 SĐT":
    phone_view.render()
elif page == "🔗 URL":
    url_view.render()

render_footer()

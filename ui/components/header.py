import streamlit as st
from config.settings import APP_NAME, APP_SUBTITLE

def render_header():
    st.markdown(
        f'''
        <div class="vdt-hero">
            <h1>🛡️ {APP_NAME}</h1>
            <p>{APP_SUBTITLE}</p>
        </div>
        ''',
        unsafe_allow_html=True,
    )

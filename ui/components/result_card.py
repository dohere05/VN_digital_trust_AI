import streamlit as st

def info_row(label: str, value):
    st.markdown(f"**{label}:** {value}")

def yes_no(value: bool) -> str:
    return "✅ Có" if value else "❌ Không"

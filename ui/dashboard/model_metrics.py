import json
from pathlib import Path
import streamlit as st

def render_metrics(metrics_file: str):
    path = Path(metrics_file)
    if not path.exists():
        st.info("Chưa có metrics.")
        return
    st.json(json.loads(path.read_text(encoding="utf-8")))

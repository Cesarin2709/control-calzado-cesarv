```python
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="BRIXTON - Control de Producción", layout="wide", page_icon="👟")

# --- ESTILOS PERSONALIZADOS ---
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; border-radius: 10px; font-weight: bold; }
    .metric-card {
        background-color: white; padding: 20px; border-radius: 15px; 
        box-shadow: 0 4px 6px rgba(0,0,0,0.1); text-align: center;
        border: 1px solid #eee;
    }
    </style>
    """, unsafe_allow_html=True)

# --- BASE DE DATOS INICIAL ---
if 'db_productos' not in st.session_state:
    st.session_state.db_productos = pd.DataFrame([
        ["63356", "START TEJIDO", "VERDE AGUA", "23/28", "NIÑOS", "Textil", "CAUCHO"],
        ["C12502101", "MESSI", "BLANCO CELESTE", "39/42", "CABALLERO", "Deportivas", "CAUCHO"],
        ["C21609101", "ZOOM 09", "NEGRO PLATA", "39/42", "CABALLERO", "Deportivas", "CAUCHO"],
        ["C22504101", "ALFA", "AM.LIMON FUCSIA", "39/42", "CABALLERO", "Deportivas", "CAUCHO"],
    ], columns=["
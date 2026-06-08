Para que no tengas problemas al copiar y pegar, he simplificado el código al máximo. 

Sigue estos pasos exactamente:

1. Ve a tu archivo `app_calzado.py` en GitHub.
2. **Borra TODO lo que tenga el archivo.**
3. Copia y pega este código completo. **He unido la Parte 1 y la Parte 2 en un solo bloque** y he reducido el tamaño para que el sistema no lo corte.

Copia desde el primer `import` hasta el final:

```python
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="BRIXTON", layout="wide", page_icon="👟")

# --- BASE DE DATOS ---
if 'db_productos' not in st.session_state:
    st.session_state.db_productos = pd.DataFrame([
        ["63356", "START TEJIDO", "VERDE AGUA", "23/28", "NIÑOS", "Textil", "CAUCHO"],
        ["C12502101", "MESSI", "BLANCO CELESTE", "39/42", "CABALLERO", "Deportivas", "CAUCHO"],
    ], columns=["codigo", "modelo", "color", "talla", "tipo", "linea", "suela"])

if 'pedidos' not in st.session_state:
    st.session_state.pedidos = pd.DataFrame(columns=["fecha", "cliente", "modelo", "color", "docenas", "pares", "estado", "sem"])

def get_week(date):
    return date.isocalendar()[1]

st.sidebar.title("👟 BRIXTON")
menu = st.sidebar.radio("Navegación", ["🏠 Panel General", "🛒 Pedidos", "📋 Órdenes", "🖼️ Catálogo"])

if menu == "🏠 Panel General":
    st.title("🚀 Panel General")
    total_ped = len(st.session_state.pedidos)
    total_doc = st.session_state.pedidos['docenas'].sum() if total_ped > 0 else 0
    col1, col2 = st.columns(2)
    col1.metric("Total Pedidos", total_ped)
    col2.metric("Total Docenas", total_doc)
    if total_ped > 0:
        
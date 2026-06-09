python
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="BRIXTON", layout="wide", page_icon="👟")

if 'db' not in st.session_state:
    st.session_state.db = pd.DataFrame([
        ["63356", "START TEJIDO", "VERDE", "23/28", "NIÑOS"],
        ["C12502101", "MESSI", "BLANCO", "39/42", "CABALLERO"],
    ], columns=["codigo", "modelo", "color", "talla", "tipo"])

if 'pedidos' not in st.session_state:
    st.session_state.pedidos = pd.DataFrame(columns=["fecha", "cliente", "modelo", "color", "doc", "estado"])

st.sidebar.title("👟 BRIXTON")
menu = st.sidebar.radio("Menú", ["🏠 Panel", "🛒 Pedidos", "📋 Órdenes", "🖼️ Catálogo"])

if menu == "🏠 Panel":
    st.title("🚀 Panel General")
    p = st.session_state.pedidos
    total = len(p)
    doc_tot = p['doc'].sum() if total > 0 else 0
    c1, c2 = st.columns(2)
    c1.metric("Pedidos", total)
    c2.metric("Docenas", int(doc_tot))
    if total > 0:
        st.plotly_chart(px.pie(p, names='estado', title="Estados"))
    else: st.info("Sin datos.")

elif menu == "🛒 Pedidos":
    st.title("🛒 Pedidos")
    with st.form("f"):
        f = st.date_input("Fecha")
        cl = st.text_input("Cliente")
        md = st.selectbox("Modelo", st.session_state.db['modelo'].tolist())
        co = st.text_input("Color")
python
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="BRIXTON Control", layout="wide", page_icon="👟")

# --- BASE DE DATOS INICIAL ---
if 'db_prod' not in st.session_state:
    st.session_state.db_prod = pd.DataFrame([
        ["63356", "START TEJIDO", "VERDE AGUA", "23/28", "NIÑOS", "Textil", "CAUCHO"],
        ["C12502101", "MESSI", "BLANCO CELESTE", "39/42", "CABALLERO", "Deportivas", "CAUCHO"],
        ["C21609101", "ZOOM 09", "NEGRO PLATA", "39/42", "CABALLERO", "Deportivas", "CAUCHO"],
    ], columns=["codigo", "modelo", "color", "talla", "tipo", "linea", "suela"])

if 'pedidos' not in st.session_state:
    st.session_state.pedidos = pd.DataFrame(columns=["fecha", "cliente", "modelo", "color", "doc", "pares", "estado", "sem"])

# --- NAVEGACIÓN ---
st.sidebar.title("👟 BRIXTON")
menu = st.sidebar.radio("Menú", ["🏠 Panel", "🛒 Pedidos", "📋 Órdenes", "🖼️ Catálogo"])

if menu == "🏠 Panel":
    st.title("🚀 Panel General")
    peds = st.session_state.pedidos
    total_p = len(peds)
    total_d = peds['doc'].sum() if total_p > 0 else 0
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Pedidos", total_p)
    c2.metric("Docenas", int(total_d))
    c3.metric("Pares", int(total_d * 12))
    
    if total_p > 0:
        fig = px.pie(peds, names='estado', title="Estado de Pedidos", hole=0.4)
        st.plotly_chart(fig)
    else:
        st.info("Registra pedidos para ver el análisis.")

elif menu == "🛒 Pedidos":
    st.title("🛒 Gestión de Pedidos")
    with st.form("f_ped"):
        col1, col2, col3 = st.columns(3)
        f = col1.date_input("Fecha")
        cl = col2.text_input("Cliente")
        md = col3.selectbox("Modelo", st.session_state.db_prod['modelo'].tolist())
        col4, col5, col6 = st.columns(3)
        co = col4.text_input("Color")
        dc = col5.number_input("Docenas", min_value=0, step=1)
        es = col6.selectbox("Estado", ["Pendiente", "En proceso", "Completado", "Cancelado"])
        
        if st.form_submit_button("Guardar Pedido"):
            nuevo = {"fecha": f, "cliente": cl, "modelo": md, "color": co, "doc": dc, "pares": dc*12, "estado": es, "sem": f.isocalendar()[1]}
            st.session_state.pedidos = pd.concat([st.session_state.pedidos, pd.DataFrame([nuevo])], ignore_index=True)
            st.success("¡Pedido Guardado!")
    st.dataframe(st.session_state.pedidos, use_container_width=True)

elif menu == "📋 Órdenes":
    st.title("📋 Órdenes de Producción")
    peds = st.session_state.pedidos
    if not peds.empty:
        sel = st.selectbox("Seleccionar Pedido", peds.index)
        p = peds.iloc[sel]
        st.markdown(f"""
        <div style="background:white; padding:20px; border:2px solid #1a3a5c; border-radius:10px; color:black">
            <h2 style="text-
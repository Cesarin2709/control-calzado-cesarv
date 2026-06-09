python
import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="BRIXTON", layout="wide")

if 'db' not in st.session_state:
    st.session_state.db = pd.DataFrame([["63356", "START"], ["C125", "MESSI"]], columns=["cod", "mod"])

if 'pedidos' not in st.session_state:
    st.session_state.pedidos = pd.DataFrame(columns=["fecha", "cliente", "modelo", "doc", "estado"])

st.sidebar.title("👟 BRIXTON")
menu = st.sidebar.radio("Menú", ["🏠 Panel", "🛒 Pedidos"])

if menu == "🏠 Panel":
    st.title("🚀 Panel General")
    st.write(f"Total pedidos: {len(st.session_state.pedidos)}")
    st.dataframe(st.session_state.pedidos, use_container_width=True)

elif menu == "🛒 Pedidos":
    st.title("🛒 Registrar Pedido")
    with st.form("mi_formulario"):
        # ESTA ES LA LINEA DE LA FECHA
        fe = st.date_input("📅 Fecha del Pedido", value=datetime.now())
        cl = st.text_input("👤 Cliente")
        md = st.selectbox("👟 Modelo", st.session_state.db['mod'].tolist())
        dc = st.number_input("📦 Docenas", min_value=0)
        es = st.selectbox("⚙️ Estado", ["Pendiente", "En Proceso", "Listo"])
        
        boton = st.form_submit_button("Guardar Pedido")
        
        if boton:
            nuevo = {"fecha": fe, "cliente": cl, "modelo": md, "doc": dc, "estado": es}
            st.session_state.pedidos = pd.concat([st.session_state.pedidos, pd.DataFrame([nuevo])], ignore_index=True)
            st.success("¡Pedido guardado con éxito!")
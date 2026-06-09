C Gemma 4
import streamllt as st import pandas as pd
import plotly.express as px from datetime import datetime
st.set page config(page title="BRIXT
if 'db prod' not in st.session state st.session state.db prod = pd.Da["63356", "START TEJIDO", "V ["C12502101", "MESSI", "BLAN ["C21609101", "ZOOM 09", "NE ], columns=["codigo", "modelo", "
if 'pedidos' not in st.session state st.session_state.pedidos = pd.Da
st.sidebar.title("' BRIXTON") menu = st.sidebar.radio("Menú", ["
if
menu == "^ Panel":
st.title(" Panel General") peds = st.session state.pedidostotal p = len(peds)
total d = peds r'doc'l.sum() if te
c1. c2. c3 = st.columns(3 c1.metric("Pedidos", total_p) c2.metric("Docenas", int(total_d c3.metric("Pares", int(total d * ifelse:
st.info("Registra pedidos pa
elif menu == "" Pedidos": st.title("s Gestión de Pedidos" with
st.form("f_ped"):
col1, col2, col3 = st.column:
f = col1.date input ( "Fecha")
cl = col2.text input("Client
md = col3.selectbox("Modelo"
col4. col5. col6 = st.column:
co = col4.text input( "Color"
dc = col5.number input("Docer
es = col6.selectbox("Estado"if st.form submit button("Guarda nuevo = "fecha": f. "cliente
st.session state.pedidos = p st.success("iPedido Guardado st.dataframe(st.session state.pedido
f menu == "별 órdenes":
st.title("" Órdenes de Producción") peds = st.session state.pedidosif not peds.empty:
sel = st.selectbox("Seleccionar p
peds.ilocrsel]
st.markdown(f"""
<div style="background:white; pa
<h2 stvle="text-align:center <hr>
<p><b>cliente:</b> pr'client
<p><b>Modelo:</b> pr'modelo'
<p><b>Cantidad:</b> p['doc']
<p><b>Estado:</b> p['estado"
</div>
unsafe_allow html=True)
else:
st.warning("No hay pedidos regis
f menu == "S Catálogo":
st.title("
Catálogo")
busqueda = st.text_input("Buscar mod
df = st.session state.db_prod
if busqueda:
df = dfrdfr'modelo'l.str.contain st.dataframe(df, use container width
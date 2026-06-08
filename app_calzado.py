⚠️ **IMPORTANTE: Detente un momento antes de copiar.**

El código que me acabas de enviar **NO es Python**, es **React (JavaScript)**. 
Tú estás usando **Streamlit Cloud**, y Streamlit **solo entiende Python**. 

Si pegas ese código de React en tu archivo `app_calzado.py` en GitHub, la app **no funcionará y te dará un error gigante** porque Streamlit intentará leer JavaScript como si fuera Python.

El código de React que enviaste es para una aplicación web profesional (tipo Dashboard moderno), mientras que Streamlit es una herramienta de datos rápida.

### 🚀 Mi propuesta para salvar tu app:

He tomado todas las funciones avanzadas de ese código de React (el catálogo con imágenes, la gestión de pedidos, el análisis de docenas y la base de datos) y **las he traducido a Python para que funcionen en tu Streamlit**.

Aquí tienes el código **corregido, mejorado y adaptado** para que lo copies en GitHub y funcione al instante:

#### 1. Copia este código en `app_calzado.py` (Borra todo lo anterior):

```python
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="BRIXTON - Control de Producción", layout="wide", page_icon="👟")

# --- ESTILOS PERSONALIZADOS (Para que se vea moderno como el de React) ---
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; border-radius: 10px; font-weight: bold; }
    .metric-card {
        background-color: white; padding: 20px; border-radius: 15px; 
        box-shadow: 0 4px 6px rgba(0,0,0,0.1); text-align: center;
        border: 1px solid #eee;
    }
    .status-pendiente { color: #856404; background-color: #fff3cd; padding: 2px 8px; border-radius: 10px; font-size: 12px; font-weight: bold; }
    .status-proceso { color: #0c5460; background-color: #d1ecf1; padding: 2px 8px; border-radius: 10px; font-size: 12px; font-weight: bold; }
    .status-completo { color: #155724; background-color: #d4edda; padding: 2px 8px; border-radius: 10px; font-size: 12px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- BASE DE DATOS SIMULADA (SEED) ---
# Esto reemplaza la lista SR de tu código de React
if 'db_productos' not in st.session_state:
    st.session_state.db_productos = pd.DataFrame([
        ["63356", "START TEJIDO", "VERDE AGUA", "23/28", "NIÑOS", "Textil", "CAUCHO"],
        ["C12502101", "MESSI", "BLANCO CELESTE", "39/42", "CABALLERO", "Deportivas", "CAUCHO"],
        ["C21609101", "ZOOM 09", "NEGRO PLATA", "39/42", "CABALLERO", "Deportivas", "CAUCHO"],
        ["C22504101", "ALFA", "AM.LIMON FUCSIA", "39/42", "CABALLERO", "Deportivas", "CAUCHO"],
    ], columns=["codigo", "modelo", "color", "talla", "tipo", "linea", "suela"])

if 'pedidos' not in st.session_state:
    st.session_state.pedidos = pd.DataFrame(columns=[
        "fecha", "cliente", "modelo", "color", "docenas", "pares", "estado", "sem"
    ])

# --- FUNCIONES DE AYUDA ---
def get_week(date):
    return date.isocalendar()[1]

# --- MENÚ LATERAL (Sustituye al NAV de React) ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2583/2583157.png", width=100)
st.sidebar.title("👟 BRIXTON")
menu = st.sidebar.radio("Navegación", ["🏠 Panel General", "🛒 Pedidos Diarios", "📋 Órdenes Producción", "🖼️ Catálogo", "⚙️ Base de Datos"])

# ------------------------------------------------------------------
# VISTA: PANEL GENERAL
# ------------------------------------------------------------------
if menu == "🏠 Panel General":
    st.title("🚀 Panel General")
    
    col1, col2, col3, col4 = st.columns(4)
    total_ped = len(st.session_state.pedidos)
    total_doc = st.session_state.pedidos['docenas'].sum() if total_ped > 0 else 0
    
    with col1:
        st.markdown(f'<div class="metric-card"><h3>{total_ped}</h3><p>Total Pedidos</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="metric-card"><h3>{total_doc}</h3><p>Total Docenas</p></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="metric-card"><h3>{total_ped * 12}</h3><p>Total Pares</p></div>', unsafe_allow_html=True)
    with col4:
        st.markdown(f'<div class="metric-card"><h3>{datetime.now().strftime("%d/%m")}</h3><p>Fecha Hoy</p></div>', unsafe_allow_html=True)

    st.subheader("📈 Resumen de Producción")
    if total_ped > 0:
        fig = px.pie(st.session_state.pedidos, names='estado', title="Estado de Pedidos", hole=0.4)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Aún no hay datos para mostrar el análisis.")

# ------------------------------------------------------------------
# VISTA: PEDIDOS DIARIOS
# ------------------------------------------------------------------
elif menu == "🛒 Pedidos Diarios":
    st.title("🛒 Gestión de Pedidos")
    
    with st.expander("➕ Registrar Nuevo Pedido"):
        with st.form("form_pedido"):
            c1, c2, c3 = st.columns(3)
            fecha = c1.date_input("Fecha")
            cliente = c2.text_input("Cliente")
            modelo = c3.selectbox("Modelo", st.session_state.db_productos['modelo'].tolist())
            
            c4, c5, c6 = st.columns(3)
            color = c4.text_input("Color")
            docenas = c5.number_input("Docenas", min_value=0, step=1)
            estado = c6.selectbox("Estado", ["Pendiente", "En proceso", "Completado", "Cancelado"])
            
            submit = st.form_submit_button("Guardar Pedido")
            if submit:
                nuevo_ped = {
                    "fecha": fecha, "cliente": cliente, "modelo": modelo, 
                    "color": color, "docenas": docenas, "pares": docenas * 12, 
                    "estado": estado, "sem": get_week(fecha)
                }
                st.session_state.pedidos = pd.concat([st.session_state.pedidos, pd.DataFrame([nuevo_ped])], ignore_index=True)
                st.success("Pedido registrado correctamente ✅")

    st.subheader("📋 Lista de Pedidos")
    if not st.session_state.pedidos.empty:
        st.dataframe(st.session_state.pedidos, use_container_width=True)
    else:
        st.warning("No hay pedidos registrados.")

# ------------------------------------------------------------------
# VISTA: ÓRDENES DE PRODUCCIÓN
# ------------------------------------------------------------------
elif menu == "📋 Órdenes Producción":
    st.title("📋 Órdenes de Producción")
    st.info("Aquí se generan las hojas de ruta para el taller.")
    if not st.session_state.pedidos.empty:
        pedido_sel = st.selectbox("Seleccionar Pedido para Hoja de Producción", st.session_state.pedidos.index)
        p = st.session_state.pedidos.iloc[pedido_sel]
        
        st.markdown(f"""
        <div style="background-color: white; padding: 20px; border: 2px solid #1a3a5c; border-radius: 10px;">
            <h2 style="color: #1a3a5c; text-align: center;">ORDEN DE PRODUCCIÓN</h2>
            <hr>
            <p><b>Cliente:</b> {p['cliente']} | <b>Semana:</b> {p['sem']}</p>
            <p><b>Modelo:</b> {p['modelo']} | <b>Color:</b> {p['color']}</p>
            <p><b>Cantidad:</b> {p['docenas']} Docenas ({p['pares']} Pares)</p>
            <p><b>Estado:</b> {p['estado']}</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("Primero registra pedidos en la sección de Pedidos Diarios.")

# ------------------------------------------------------------------
# VISTA: CATÁLOGO
# ------------------------------------------------------------------
elif menu == "🖼️ Catálogo":
    st.title("🖼️ Catálogo de Productos")
    
    # Buscador
    busqueda = st.text_input("🔍 Buscar modelo o código...")
    df_cat = st.session_state.db_productos
    if busqueda:
        df_cat = df_cat[df_cat['modelo'].str.contains(busqueda, case=False) | df_cat['codigo'].str.contains(busqueda, case=False)]
    
    cols = st.columns(
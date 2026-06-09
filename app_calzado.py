
import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="BRIXTON Control", layout="wide", page_icon="👟")

# --- CARGA DE DATOS DEL EXCEL ---
@st.cache_data
def cargar_catalogo():
    try:
        # Usamos el nombre simplificado para evitar errores de lectura
        df = pd.read_excel("catalogo.xlsx")
        # Convertimos todos los nombres de columnas a MAYÚSULAS y quitamos espacios
        df.columns = [str(c).strip().upper() for c in df.columns]
        return df
    except Exception as e:
        st.error(f"❌ Error: No se encontró el archivo 'catalogo.xlsx' en GitHub. {e}")
        return pd.DataFrame()

df_catalogo = cargar_catalogo()

# Base de datos de pedidos en memoria
if 'pedidos' not in st.session_state:
    st.session_state.pedidos = pd.DataFrame(columns=["fecha", "cliente", "modelo", "codigo", "color", "doc", "estado"])

# --- NAVEGACIÓN ---
st.sidebar.title("👟 BRIXTON")
menu = st.sidebar.radio("Menú", ["🏠 Panel", "🛒 Pedidos", "🖼️ Catálogo"])

if menu == "🏠 Panel":
    st.title("🚀 Panel General")
    if not st.session_state.pedidos.empty:
        st.write(f"Total de pedidos registrados: **{len(st.session_state.pedidos)}**")
        st.dataframe(st.session_state.pedidos, use_container_width=True)
    else:
        st.info("Aún no hay pedidos registrados.")

elif menu == "🛒 Pedidos":
    st.title("🛒 Registrar Pedido")
    
    if df_catalogo.empty:
        st.error("⚠️ El catálogo no está cargado. Verifica que el archivo se llame 'catalogo.xlsx' en GitHub.")
    else:
        with st.form("form_pedido"):
            col1, col2 = st.columns(2)
            with col1:
                fe = st.date_input("📅 Fecha", value=datetime.now())
                cl = st.text_input("👤 Cliente")
            
            with col2:
                # 1. FILTRO DE MODELOS: Solo muestra modelos únicos del Excel
                if 'MODELO' in df_catalogo.columns:
                    modelos = sorted(df_catalogo['MODELO'].unique().tolist())
                    md_sel = st.selectbox("👟 Seleccione Modelo", modelos)
                    
                    # 2. FILTRO DINÁMICO: Buscar colores y códigos asociados a ese modelo
                    datos_modelo = df_catalogo[df_catalogo['MODELO'] == md_sel]
                    
                    # Creamos una lista de opciones: "CÓDIGO - COLOR"
                    opciones_color = []
                    for _, fila in datos_modelo.iterrows():
                        cod = str(fila.get('CODIGO', 'S/N'))
                        col = str(fila.get('COLOR', 'S/N'))
                        opciones_color.append(f"{cod} - {col}")
                    
                    col_sel = st.selectbox("🎨 Color y Código", opciones_color)
                else:
                    st.error("La columna 'MODELO' no existe en el Excel.")
                    md_sel = ""
                    col_sel = ""

            dc = st.number_input("📦 Docenas", min_value=0, step=1)
            es = st.selectbox("⚙️ Estado", ["Pendiente", "En Proceso", "Listo", "Entregado"])
            
            boton = st.form_submit_button("✅ Guardar Pedido")
            
            if boton:
                if md_sel and col_sel:
                    # Separamos el código y el color del string seleccionado
                    codigo_final, color_final = col_sel.split(" - ")
                    
                    nuevo = {
                        "fecha": fe, "cliente": cl, "modelo": md_sel, 
                        "codigo": codigo_final, "color": color
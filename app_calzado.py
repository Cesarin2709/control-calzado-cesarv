import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="BRIXTON Control", layout="wide", page_icon="👟")

# --- CARGA DE DATOS DEL EXCEL ---
@st.cache_data
def cargar_catalogo():
    try:
        # CAMBIO: Ahora busca el archivo 300.xlsx
        df = pd.read_excel("300.xlsx")
        # Limpiar nombres de columnas: Quitar espacios y poner en MAYÚSULAS
        df.columns = [str(c).strip().upper() for c in df.columns]
        return df
    except Exception as e:
        st.error(f"❌ Error: No se encontró el archivo '300.xlsx' en GitHub. {e}")
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
        st.error("⚠️ El archivo '300.xlsx' no está cargado o está vacío.")
    else:
        with st.form("form_pedido"):
            col1, col2 = st.columns(2)
            with col1:
                fe = st.date_input("📅 Fecha", value=datetime.now())
                cl = st.text_input("👤 Cliente")
            
            with col2:
                # Buscamos la columna MODELO en el Excel
                if 'MODELO' in df_catalogo.columns:
                    modelos = sorted(df_catalogo['MODELO'].unique().tolist())
                    md_sel = st.selectbox("👟 Seleccione Modelo", modelos)
                    
                    # Filtrar colores y códigos según el modelo seleccionado
                    datos_modelo = df_catalogo[df_catalogo['MODELO'] == md_sel]
                    
                    opciones_color = []
                    for _, fila in datos_modelo.iterrows():
                        cod = str(fila.get('CODIGO', 'S/N'))
                        col = str(fila.get('COLOR', 'S/N'))
                        opciones_color.append(f"{cod} - {col}")
                    
                    col_sel = st.selectbox("🎨 Color y Código", opciones_color)
                else:
                    st.error("La columna 'MODELO' no existe en el archivo 300.xlsx")
                    md_sel = col_sel = ""

            dc = st.number_input("📦 Docenas", min_value=0, step=1)
            es = st.selectbox("⚙️ Estado", ["Pendiente", "En Proceso", "Listo", "Entregado"])
            
            boton = st.form_submit_button("✅ Guardar Pedido")
            
            if boton:
                if md_sel and col_sel:
                    codigo_final, color_final = col_sel.split(" - ")
                    nuevo = {
                        "fecha": fe, "cliente": cl, "modelo": md_sel, 
                        "codigo": codigo_final, "color": color_final, 
                        "doc": dc, "estado": es
                    }
                    st.session_state.pedidos = pd.concat([st.session_state.pedidos, pd.DataFrame([nuevo])], ignore_index=True)
                    st.success(f"✅ Pedido guardado con éxito!")
                else:
                    st.warning("Por favor selecciona un modelo y color.")

elif menu == "🖼️ Catálogo":
    st.title("🖼️ Catálogo Maestro (300.xlsx)")
    if not df_catalogo.empty:
        busqueda = st.text_input("🔍 Buscar modelo, código o color...")
        if busqueda:
            filtro = df_catalogo[df_catalogo.apply(lambda row: busqueda.lower() in str(row).lower(), axis=1)]
            st.dataframe(filtro,  
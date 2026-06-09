
import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="BRIXTON Control", layout="wide", page_icon="👟")

# --- CARGA DE DATOS DEL EXCEL ---
@st.cache_data
def cargar_catalogo():
    try:
        # Leemos el Excel. Ajusta el nombre si es diferente en GitHub
        df = pd.read_excel("BRIXTON CATALOGO 2026A.xlsx")
        # Limpiamos nombres de columnas para evitar errores
        df.columns = [c.strip().upper() for c in df.columns]
        return df
    except Exception as e:
        st.error(f"Error al cargar Excel: {e}")
        return pd.DataFrame()

df_catalogo = cargar_catalogo()

if 'pedidos' not in st.session_state:
    st.session_state.pedidos = pd.DataFrame(columns=["fecha", "cliente", "modelo", "codigo", "color", "doc", "estado"])

# --- NAVEGACIÓN ---
st.sidebar.title("👟 BRIXTON")
menu = st.sidebar.radio("Menú", ["🏠 Panel", "🛒 Pedidos", "🖼️ Catálogo"])

if menu == "🏠 Panel":
    st.title("🚀 Panel General")
    st.write(f"Total pedidos registrados: {len(st.session_state.pedidos)}")
    st.dataframe(st.session_state.pedidos, use_container_width=True)

elif menu == "🛒 Pedidos":
    st.title("🛒 Registrar Pedido")
    
    if df_catalogo.empty:
        st.warning("Carga el archivo 'BRIXTON CATALOGO 2026A.xlsx' en GitHub para activar el catálogo.")
    else:
        with st.form("form_pedido"):
            fe = st.date_input("📅 Fecha", value=datetime.now())
            cl = st.text_input("👤 Cliente")
            
            # 1. Filtro de Modelos (Únicos)
            modelos = df_catalogo['MODELO'].unique().tolist()
            md_sel = st.selectbox("👟 Seleccione Modelo", modelos)
            
            # 2. Filtro Dinámico de Colores y Códigos basado en el modelo
            # Filtramos el catálogo para obtener solo las filas del modelo seleccionado
            datos_modelo = df_catalogo[df_catalogo['MODELO'] == md_sel]
            
            # Creamos una lista de opciones: "CÓDIGO - COLOR"
            opciones_color = datos_modelo.apply(lambda x: f"{x['CODIGO']} - {x['COLOR']}", axis=1).tolist()
            
            col_sel = st.selectbox("🎨 Color y Código", opciones_color)
            
            dc = st.number_input("📦 Docenas", min_value=0)
            es = st.selectbox("⚙️ Estado", ["Pendiente", "En Proceso", "Listo"])
            
            boton = st.form_submit_button("Guardar Pedido")
            
            if boton:
                # Extraemos el código y color del string seleccionado
                codigo_final = col_sel.split(" - ")[0]
                color_final = col_sel.split(" - ")[1]
                
                nuevo = {
                    "fecha": fe, "cliente": cl, "modelo": md_sel, 
                    "codigo": codigo_final, "color": color_final, 
                    "doc": dc, "estado": es
                }
                st.session_state.pedidos = pd.concat([st.session_state.pedidos, pd.DataFrame([nuevo])], ignore_index=True)
                st.success(f"Pedido de {md_sel} ({color_final}) guardado!")

elif menu == "🖼️ Catálogo":
    st.title("🖼️ Catálogo Maestro")
    if not df_catalogo.empty:
        busqueda = st.text_input("Buscar modelo o código...")
        if busqueda:
            filtro = df_catalogo[df_catalogo['MODELO'].str.contains(busqueda, case=False) | 
                                 df_catalogo['CODIGO'].astype(str).str.contains(busqueda)]
            st.dataframe(filtro)
        else:
            st.dataframe(df_catalogo)
    else:
        st.info("No hay catálogo disponible.")

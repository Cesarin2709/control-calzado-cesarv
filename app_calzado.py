import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="BRIXTON Control", layout="wide", page_icon="👟")

@st.cache_data
def cargar_catalogo():
    try:
        df = pd.read_excel("catalogo.xlsx")
        df.columns = [str(c).strip().upper() for c in df.columns]
        return df
    except Exception as e:
        st.error(f"❌ Error: No se encontró 'catalogo.xlsx' en GitHub. {e}")
        return pd.DataFrame()

df_catalogo = cargar_catalogo()

if 'pedidos' not in st.session_state:
    st.session_state.pedidos = pd.DataFrame(columns=["fecha", "cliente", "modelo", "codigo", "color", "doc", "estado"])

st.sidebar.title("👟 BRIXTON")
menu = st.sidebar.radio("Menú", ["🏠 Panel", "🛒 Pedidos", "🖼️ Catálogo"])

if menu == "🏠 Panel":
    st.title("🚀 Panel General")
    if not st.session_state.pedidos.empty:
        st.write(f"Total de pedidos registrados: **{len(st.session_state.pedidos)}**")
        st.dataframe(st.session_state.pedidos, use_container_width=True)
    else:
        st.info("Aún no hay pedidos registrados.")
```

---

### 📦 PARTE 2 (Pégala justo debajo de la Parte 1)

```python
elif menu == "🛒 Pedidos":
    st.title("🛒 Registrar Pedido")
    if df_catalogo.empty:
        st.error("⚠️ El catálogo no está cargado. Verifica el archivo 'catalogo.xlsx' en GitHub.")
    else:
        with st.form("form_pedido"):
            col1, col2 = st.columns(2)
            with col1:
                fe = st.date_input("📅 Fecha", value=datetime.now())
                cl = st.text_input("👤 Cliente")
            with col2:
                if 'MODELO' in df_catalogo.columns:
                    modelos = sorted(df_catalogo['MODELO'].unique().tolist())
                    md_sel = st.selectbox("👟 Seleccione Modelo", modelos)
                    datos_modelo = df_catalogo[df_catalogo['MODELO'] == md_sel]
                    opciones_color = [f"{str(f.get('CODIGO','S/N'))} - {str(f.get('COLOR','S/N'))}" for _, f in datos_modelo.iterrows()]
                    col_sel = st.selectbox("🎨 Color y Código", opciones_color)
                else:
                    st.error("No existe columna 'MODELO' en el Excel.")
                    md_sel = col_sel = ""

            dc = st.number_input("📦 Docenas", min_value=0, step=1)
            es = st.selectbox("⚙️ Estado", ["Pendiente", "En Proceso", "Listo", "Entregado"])
            boton = st.form_submit_button("✅ Guardar Pedido")
            
            if boton:
                if md_sel and col_sel:
                    codigo_final, color_final = col_sel.split(" - ")
                    nuevo = {"fecha": fe, "cliente": cl, "modelo": md_sel, "codigo": codigo_final, "color": color_final, "doc": dc, "estado": es}
                    st.session_state.pedidos = pd.concat([st.session_state.pedidos, pd.DataFrame([nuevo])], ignore_index=True)
                    st.success(f"✅ Pedido guardado: {md_sel}")

elif menu == "🖼️ Catálogo":
    st.title("🖼️ Catálogo Maestro")
    if not df_catalogo.empty:
        busqueda = st.text_input("🔍 Buscar modelo, código o color...")
        if busqueda:
            filtro = df_catalogo[df_catalogo.apply(lambda row: busqueda.lower() in str(row).lower(), axis=1)]
            st.dataframe(filtro, use_container_width=True)
        else:
            st.dataframe(df_catalogo, use_container_width=True)
    else:
        st.info("No hay catálogo disponible.")



import streamlit as st
import pandas as pd
import plotly.express as px
import os
from datetime import datetime

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Footwear Production OS", layout="wide")

# --- GESTIÓN DE BASE DE DATOS (SIMULADA CON CSV) ---
CATALOGO_FILE = "catalogo_modelos.csv"
PEDIDOS_FILE = "pedidos_produccion.csv"

def load_data(file):
    if os.path.exists(file):
        return pd.read_csv(file)
    return pd.DataFrame()

def save_data(df, file):
    df.to_csv(file, index=False)

# Carga inicial de datos
df_catalogo = load_data(CATALOGO_FILE)
df_pedidos = load_data(PEDIDOS_FILE)

# --- INTERFAZ LATERAL (NAVEGACIÓN) ---
st.sidebar.title("👞 Footwear OS")
menu = st.sidebar.selectbox("Menú de Navegación", 
                           ["🏠 Dashboard", "📦 Ingresar Pedido", "📚 Catálogo y Base de Datos"])

# ==========================================
# PESTAÑA 1: CATÁLOGO Y BASE DE DATOS
# ==========================================
if menu == "📚 Catálogo y Base de Datos":
    st.header("📚 Gestión de Catálogo")
    st.info("Registra aquí tus modelos y colores para que aparezcan en el menú de pedidos.")
    
    with st.form("form_catalogo"):
        col1, col2 = st.columns(2)
        with col1:
            modelo = st.text_input("Nombre del Modelo (Ej: PRODISSION 2026)")
            referencia = st.text_input("Referencia/Código (Ej: J2250701)")
        with col2:
            color = st.text_input("Color (Ej: Rojo Blanco Negro Assassin)")
            categoria = st.selectbox("Categoría", ["Master", "Prodission", "Otros"])
        
        submit_cat = st.form_submit_button("Guardar en Catálogo")
        
        if submit_cat:
            nuevo_item = pd.DataFrame([[modelo, referencia, color, categoria]], 
                                     columns=["Modelo", "Referencia", "Color", "Categoria"])
            df_catalogo = pd.concat([df_catalogo, nuevo_item], ignore_index=True)
            save_data(df_catalogo, CATALOGO_FILE)
            st.success("Modelo guardado exitosamente.")

    st.subheader("Base de Datos Actual")
    st.dataframe(df_catalogo, use_container_width=True)

# ==========================================
# PESTAÑA 2: INGRESAR PEDIDO
# ==========================================
elif menu == "📦 Ingresar Pedido":
    st.header("📦 Registro de Nueva Orden")
    
    if df_catalogo.empty:
        st.warning("Primero debes agregar modelos en la pestaña de Catálogo.")
    else:
        with st.form("form_pedido"):
            col1, col2, col3 = st.columns(3)
            with col1:
                fecha = st.date_input("Fecha de Orden", datetime.now())
            with col2:
                # Buscador inteligente de modelos del catálogo
                opciones_modelos = df_catalogo['Modelo'].unique()
                modelo_sel = st.selectbox("Selecciona Modelo", opciones_modelos)
            with col3:
                # Filtra colores disponibles para ese modelo seleccionado
                colores_disponibles = df_catalogo[df_catalogo['Modelo'] == modelo_sel]['Color'].unique()
                color_sel = st.selectbox("Selecciona Color", colores_disponibles)

            st.divider()
            st.subheader("Seriado de Tallas")
            # Definimos tallas comunes
            tallas = ["35", "36", "37", "38", "39", "40", "41", "42", "43", "44"]
            cols_tallas = st.columns(len(tallas))
            
            cantidades = {}
            for i, talla in enumerate(tallas):
                with cols_tallas[i]:
                    cantidades[talla] = st.number_input(f"T_{talla}", min_value=0, step=1)

            # Cálculos Automáticos
            total_pares = sum(cantidades.values())
            total_docenas = total_pares / 12

            st.write(f"**Total Pares:** {total_pares} | **Total Docenas:** {total_docenas:.2f}")
            
            submit_pedido = st.form_submit_button("Confirmar y Guardar Orden")
            
            if submit_pedido:
                # Creamos una fila por cada talla que tenga cantidad > 0
                nuevos_pedidos = []
                for t, c in cantidades.items():
                    if c > 0:
                        nuevos_pedidos.append([fecha, modelo_sel, color_sel, t, c])
                
                df_nuevos = pd.DataFrame(nuevos_pedidos, columns=["Fecha", "Modelo", "Color", "Talla", "Cantidad"])
                df_pedidos = pd.concat([df_pedidos, df_nuevos], ignore_index=True)
                save_data(df_pedidos, PEDIDOS_FILE)
                st.success(f"Orden de {modelo_sel} guardada correctamente.")

# ==========================================
# PESTAÑA 3: DASHBOARD INTERACTIVO
# ==========================================
elif menu == "🏠 Dashboard":
    st.header("📊 Análisis de Producción")
    
    if df_pedidos.empty:
        st.info("Aún no hay datos de pedidos para analizar.")
    else:
        # KPIs Superiores
        kpi1, kpi2, kpi3 = st.columns(3)
        kpi1.metric("Total Pares Producidos", int(df_pedidos['Cantidad'].sum()))
        kpi2.metric("Modelos Activos", df_pedidos['Modelo'].nunique())
        kpi3.metric("Colores Diversos", df_pedidos['Color'].nunique())

        st.divider()

        # Gráfico 1: Modelos más pedidos
        st.subheader("🔝 Modelos más demandados")
        fig_modelos = px.bar(df_pedidos.groupby("Modelo")["Cantidad"].sum().reset_index(), 
                             x="Modelo", y="Cantidad", color="Modelo", 
                             title="Cantidad de Pares por Modelo")
        st.plotly_chart(fig_modelos, use_container_width=True)

        # Gráfico 2: Colores más pedidos
        st.subheader("🎨 Análisis de Colores")
        fig_colores = px.pie(df_pedidos.groupby("Color")["Cantidad"].sum().reset_index(), 
                            values="Cantidad", names="Color", title="Distribución de Colores")
        st.plotly_chart(fig_colores, use_container_width=True)

        # Gráfico 3: Tallas Críticas
        st.subheader("📏 Análisis de Tallas")
        fig_tallas = px.bar(df_pedidos.groupby("Talla")["Cantidad"].sum().reset_index(), 
                            x="Talla", y="Cantidad", color_discrete_sequence=['#00CC96'])
        st.plotly_chart(fig_tallas, use_container_width=True)

        # Tabla Detallada Final
        st.subheader("📄 Detalle Completo de Órdenes")
        st.dataframe(df_pedidos, use_container_width=True)



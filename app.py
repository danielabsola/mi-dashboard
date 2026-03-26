import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

# Título de la página
st.set_page_config(page_title="Mi Dashboard", layout="wide")
st.title("📊 Dashboard de Ventas")

# Datos de ejemplo
np.random.seed(42)
fechas = pd.date_range("2023-01-01", periods=100, freq="D")
ventas = np.random.randint(100, 500, size=len(fechas))
categorias = np.random.choice(["Electrónica", "Ropa", "Hogar"], size=len(fechas))

df = pd.DataFrame({
    "Fecha": fechas,
    "Ventas": ventas,
    "Categoría": categorias
})

# Sidebar con filtros
st.sidebar.header("Filtros")
categoria_seleccionada = st.sidebar.multiselect(
    "Selecciona categoría",
    options=df["Categoría"].unique(),
    default=df["Categoría"].unique()
)

rango_fechas = st.sidebar.date_input(
    "Rango de fechas",
    [df["Fecha"].min(), df["Fecha"].max()]
)

# Filtrar datos
df_filtrado = df[
    (df["Categoría"].isin(categoria_seleccionada)) &
    (df["Fecha"] >= pd.to_datetime(rango_fechas[0])) &
    (df["Fecha"] <= pd.to_datetime(rango_fechas[1]))
]

# Mostrar métricas
col1, col2, col3 = st.columns(3)
col1.metric("Ventas totales", f"${df_filtrado['Ventas'].sum():,.0f}")
col2.metric("Ventas promedio", f"${df_filtrado['Ventas'].mean():,.0f}")
col3.metric("Número de transacciones", len(df_filtrado))

# Gráfico de líneas (ventas diarias)
st.subheader("Evolución de ventas")
chart = alt.Chart(df_filtrado).mark_line().encode(
    x="Fecha:T",
    y="Ventas:Q",
    color="Categoría:N"
).interactive()
st.altair_chart(chart, use_container_width=True)

# Tabla de datos
st.subheader("Datos filtrados")
st.dataframe(df_filtrado)

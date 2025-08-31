import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Resumen del Proyecto", page_icon="📊", layout="wide")
st.title("📊 Resumen General del Proyecto Inmobiliario")
# --- Barra lateral para la entrada de datos ---
st.sidebar.header("Parámetros Generales")
# Usamos st.session_state para recordar los valores entre páginas
st.session_state.cantidad_viviendas = st.sidebar.number_input("Cantidad de Viviendas a Construir", min_value=1, value=st.session_state.get('cantidad_viviendas', 10), step=1)
st.session_state.costo_terreno = st.sidebar.number_input("Costo del Terreno ($)", min_value=0.0, value=st.session_state.get('costo_terreno', 100000.0), step=1000.0, help="Valor de compra del terreno o lote.")
st.session_state.otros_gastos = st.sidebar.number_input("Otros Gastos e Imprevistos ($)", min_value=0.0, value=st.session_state.get('otros_gastos', 15000.0), step=500.0, help="Un colchón para imprevistos y otros gastos no categorizados.")

# Asignamos a variables locales para facilitar la lectura del código
cantidad_viviendas = st.session_state.cantidad_viviendas
costo_terreno = st.session_state.costo_terreno
otros_gastos = st.session_state.otros_gastos
st.sidebar.info("Usa las otras páginas para detallar los costos de construcción, gastos administrativos y permisos.")

st.sidebar.subheader("Ingresos y Financiamiento")
st.session_state.precio_venta_unitario = st.sidebar.number_input("Precio de Venta por Vivienda ($)", min_value=0.0, value=st.session_state.get('precio_venta_unitario', 85000.0), step=1000.0)
st.session_state.monto_prestamo = st.sidebar.number_input("Monto del Préstamo ($)", min_value=0.0, value=st.session_state.get('monto_prestamo', 200000.0), step=1000.0)
st.session_state.tasa_interes_anual = st.sidebar.slider("Tasa de Interés Anual del Préstamo (%)", 0.0, 20.0, st.session_state.get('tasa_interes_anual', 5.0), 0.1)
st.session_state.plazo_prestamo_anios = st.sidebar.slider("Plazo del Préstamo (años)", 1, 30, st.session_state.get('plazo_prestamo_anios', 15))

# Asignamos a variables locales para facilitar la lectura del código
precio_venta_unitario = st.session_state.precio_venta_unitario
monto_prestamo = st.session_state.monto_prestamo
tasa_interes_anual = st.session_state.tasa_interes_anual
plazo_prestamo_anios = st.session_state.plazo_prestamo_anios

# --- Obtener totales de las otras páginas usando st.session_state ---
costo_urbanizacion = st.session_state.get('total_urbanizacion', 0.0)
costo_construccion_unitario = st.session_state.get('total_construccion_unitaria', 0.0)
gastos_admin_permisos = st.session_state.get('total_gastos_admin_permisos', 0.0)

# --- Cálculos Financieros ---
costo_total_construccion = costo_construccion_unitario * cantidad_viviendas
costo_total_inversion = costo_terreno + costo_urbanizacion + costo_total_construccion + gastos_admin_permisos + otros_gastos
ingresos_totales = precio_venta_unitario * cantidad_viviendas
utilidad_bruta = ingresos_totales - costo_total_inversion
capital_propio = costo_total_inversion - monto_prestamo

# --- Visualización en la página principal ---
st.header("Resumen Financiero")

col1, col2, col3 = st.columns(3)
col1.metric("Ingresos Totales por Ventas", f"${ingresos_totales:,.2f}")
col2.metric("Costo Total de Inversión", f"${costo_total_inversion:,.2f}")
col3.metric("Utilidad Bruta Estimada", f"${utilidad_bruta:,.2f}", delta_color="normal")

st.header("Desglose de la Inversión")

inversion_data = {
    'Categoría': ['Terreno', 'Urbanización', 'Construcción Total', 'Gastos Admin/Permisos', 'Otros/Imprevistos'],
    'Monto': [costo_terreno, costo_urbanizacion, costo_total_construccion, gastos_admin_permisos, otros_gastos]
}

fig = px.pie(inversion_data, values='Monto', names='Categoría', title='Distribución de Costos de Inversión', hole=.3)
st.plotly_chart(fig, use_container_width=True)

st.info("Navega a las otras páginas en el menú de la izquierda para detallar cada sección y ver el análisis completo.")

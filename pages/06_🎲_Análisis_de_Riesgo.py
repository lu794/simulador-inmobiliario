import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(layout="wide")
st.title("🎲 Análisis de Riesgo y Sensibilidad")
st.markdown("""
Simula cómo cambiarían los resultados de tu proyecto ante escenarios adversos o favorables. 
Ajusta los controles en la barra lateral para ver el impacto inmediato en la rentabilidad.
""")

# --- Obtener datos base de st.session_state ---
# Ingresos
cantidad_viviendas_base = st.session_state.get('cantidad_viviendas', 10)
precio_venta_unitario_base = st.session_state.get('precio_venta_unitario', 85000.0)
# Costos
costo_terreno_base = st.session_state.get('costo_terreno', 100000.0)
costo_urbanizacion_base = st.session_state.get('total_urbanizacion', 84650.0)
costo_construccion_base = st.session_state.get('total_construccion_unitaria', 25850.0) * cantidad_viviendas_base
gastos_admin_permisos_base = st.session_state.get('total_gastos_admin_permisos', 90100.0)
# Financiamiento
monto_prestamo_base = st.session_state.get('monto_prestamo', 200000.0)


# --- Parámetros de Simulación de Riesgo (Inputs del Usuario) ---
st.sidebar.header("Variables de Sensibilidad")
sobrecosto_construccion_pct = st.sidebar.slider("Sobrecosto de Construcción (%)", -10, 50, 0, 5)
variacion_precio_venta_pct = st.sidebar.slider("Variación en Precio de Venta (%)", -30, 30, 0, 5)
impuesto_renta_pct = st.sidebar.slider("Impuesto Sobre la Renta (%)", 0, 50, 25, 1, help="Tasa de impuesto a aplicar sobre la utilidad bruta.")

# --- Cálculos del Escenario Base ---
ingresos_totales_base = cantidad_viviendas_base * precio_venta_unitario_base
costo_total_base = costo_terreno_base + costo_urbanizacion_base + costo_construccion_base + gastos_admin_permisos_base
utilidad_bruta_base = ingresos_totales_base - costo_total_base
impuesto_base = utilidad_bruta_base * (impuesto_renta_pct / 100) if utilidad_bruta_base > 0 else 0
utilidad_neta_base = utilidad_bruta_base - impuesto_base
capital_propio_base = costo_total_base - monto_prestamo_base
roi_base = (utilidad_neta_base / capital_propio_base) * 100 if capital_propio_base > 0 else float('inf')

# --- Cálculos del Escenario Simulado ---
precio_venta_unitario_sc = precio_venta_unitario_base * (1 + variacion_precio_venta_pct / 100)
costo_construccion_sc = costo_construccion_base * (1 + sobrecosto_construccion_pct / 100)

ingresos_totales_sc = cantidad_viviendas_base * precio_venta_unitario_sc
costo_total_sc = costo_terreno_base + costo_urbanizacion_base + costo_construccion_sc + gastos_admin_permisos_base
utilidad_bruta_sc = ingresos_totales_sc - costo_total_sc
impuesto_sc = utilidad_bruta_sc * (impuesto_renta_pct / 100) if utilidad_bruta_sc > 0 else 0
utilidad_neta_sc = utilidad_bruta_sc - impuesto_sc
capital_propio_sc = costo_total_sc - monto_prestamo_base
roi_sc = (utilidad_neta_sc / capital_propio_sc) * 100 if capital_propio_sc > 0 else float('inf')

# --- Visualización de Resultados ---
st.header("Comparación de Escenarios")
st.write("Compara los resultados del proyecto original (Caso Base) con el escenario que has simulado.")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Caso Base")
    st.metric("Utilidad Neta Estimada", f"${utilidad_neta_base:,.2f}")
    st.metric("Retorno sobre Capital (ROI)", f"{roi_base:.2f}%")
    st.metric("Costo Total", f"${costo_total_base:,.2f}")
    st.metric("Ingresos Totales", f"${ingresos_totales_base:,.2f}")

with col2:
    st.subheader("🎲 Escenario Simulado")
    st.metric(
        "Utilidad Neta Estimada",
        f"${utilidad_neta_sc:,.2f}",
        delta=f"${utilidad_neta_sc - utilidad_neta_base:,.2f}"
    )
    st.metric(
        "Retorno sobre Capital (ROI)",
        f"{roi_sc:.2f}%",
        delta=f"{roi_sc - roi_base:.2f}%"
    )
    st.metric(
        "Costo Total",
        f"${costo_total_sc:,.2f}",
        delta=f"${costo_total_sc - costo_total_base:,.2f}"
    )
    st.metric(
        "Ingresos Totales",
        f"${ingresos_totales_sc:,.2f}",
        delta=f"${ingresos_totales_sc - ingresos_totales_base:,.2f}"
    )

st.warning(f"""
**Análisis del Escenario:**
- Un sobrecosto en construcción del **{sobrecosto_construccion_pct}%** y una variación en ventas del **{variacion_precio_venta_pct}%**...
- ...resultan en una variación de la utilidad neta de **${utilidad_neta_sc - utilidad_neta_base:,.2f}**.
- El ROI del proyecto cambia de **{roi_base:.2f}%** a **{roi_sc:.2f}%**.
""")

st.info("Nota: Este análisis introduce el cálculo de la Utilidad Neta (después de impuestos), un indicador clave solicitado en tu descripción inicial.")

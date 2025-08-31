import streamlit as st
import pandas as pd
import numpy as np
import numpy_financial as npf
import plotly.express as px

st.set_page_config(layout="wide")
st.title("🚀 Dashboard Ejecutivo del Proyecto")
st.markdown("Esta es la vista de 30,000 pies de altura. Resume los indicadores financieros y de viabilidad más importantes de todo el proyecto.")

# --- Contenedor para verificar si los datos están cargados ---
if 'total_urbanizacion' not in st.session_state:
    st.warning("Por favor, navega primero por las páginas de 'Costos' y 'Gastos' para cargar todos los datos del proyecto.")
    st.stop()

# --- 1. RECOPILAR Y CALCULAR TODOS LOS KPIs ---

# --- Obtener datos base de st.session_state ---
cantidad_viviendas = st.session_state.get('cantidad_viviendas', 10)
precio_venta_unitario = st.session_state.get('precio_venta_unitario', 85000.0)
costo_terreno = st.session_state.get('costo_terreno', 100000.0)
costo_urbanizacion = st.session_state.get('total_urbanizacion', 84650.0)
costo_construccion_unitario = st.session_state.get('total_construccion_unitaria', 25850.0)
gastos_admin_permisos = st.session_state.get('total_gastos_admin_permisos', 90100.0)
monto_prestamo = st.session_state.get('monto_prestamo', 200000.0)
tasa_interes_anual = st.session_state.get('tasa_interes_anual', 5.0)
plazo_prestamo_anios = st.session_state.get('plazo_prestamo_anios', 15)

# --- Cálculos de Rentabilidad ---
costo_total_construccion = costo_construccion_unitario * cantidad_viviendas
ingresos_totales = precio_venta_unitario * cantidad_viviendas
costo_total_inversion = costo_terreno + costo_urbanizacion + costo_total_construccion + gastos_admin_permisos
capital_propio = costo_total_inversion - monto_prestamo
utilidad_bruta = ingresos_totales - costo_total_inversion

# Para Utilidad Neta, necesitamos el impuesto. Usaremos el de la página de riesgo o un default.
impuesto_renta_pct = st.session_state.get('impuesto_renta_pct', 25.0)
impuesto_calculado = utilidad_bruta * (impuesto_renta_pct / 100) if utilidad_bruta > 0 else 0
utilidad_neta = utilidad_bruta - impuesto_calculado

# ROI y ROC
roi = (utilidad_neta / capital_propio) * 100 if capital_propio > 0 else float('inf')
roc = (utilidad_bruta / costo_total_inversion) * 100 if costo_total_inversion > 0 else 0

# --- Cálculo de la Máxima Necesidad de Capital (del Flujo de Caja) ---
# Replicamos la lógica del flujo de caja para obtener el KPI
duracion_total_meses = 36 # Usamos un default o lo traemos de session_state si lo guardamos allí
meses = np.arange(1, duracion_total_meses + 1)
flujo_df = pd.DataFrame(index=meses)
flujo_df['Flujo Neto Mensual'] = 0.0
# Simplificamos la distribución para el dashboard
flujo_df.loc[1, 'Flujo Neto Mensual'] += -costo_terreno - gastos_admin_permisos
flujo_df.loc[2, 'Flujo Neto Mensual'] += monto_prestamo
flujo_df.loc[2:6, 'Flujo Neto Mensual'] += -costo_urbanizacion / 5
flujo_df.loc[7:24, 'Flujo Neto Mensual'] += -costo_total_construccion / 18
flujo_df.loc[18:36, 'Flujo Neto Mensual'] += ingresos_totales / 19
# Pagos del préstamo
if monto_prestamo > 0 and tasa_interes_anual > 0:
    tasa_mensual = (tasa_interes_anual / 100) / 12
    n_pagos = plazo_prestamo_anios * 12
    pago_mensual = -npf.pmt(tasa_mensual, n_pagos, monto_prestamo)
    flujo_df.loc[3:duracion_total_meses, 'Flujo Neto Mensual'] += -pago_mensual

flujo_df['Flujo Acumulado'] = flujo_df['Flujo Neto Mensual'].cumsum()
maxima_necesidad_capital = flujo_df['Flujo Acumulado'].min()


# --- 2. MOSTRAR EL DASHBOARD ---

st.header("Indicadores Clave de Rentabilidad")
kpi1, kpi2, kpi3, kpi4 = st.columns(4)
kpi1.metric("Utilidad Neta (Post-Impuestos)", f"${utilidad_neta:,.2f}")
kpi2.metric("Retorno sobre Capital (ROI)", f"{roi:.2f}%")
kpi3.metric("Rentabilidad sobre Costo (ROC)", f"{roc:.2f}%")
kpi4.metric("Utilidad Bruta", f"${utilidad_bruta:,.2f}")

st.header("Métricas Clave del Proyecto")
met1, met2, met3, met4 = st.columns(4)
met1.metric("Ingresos Totales por Ventas", f"${ingresos_totales:,.2f}")
met2.metric("Costo Total de Inversión", f"${costo_total_inversion:,.2f}")
met3.metric("Capital Propio Requerido", f"${capital_propio:,.2f}")
met4.metric("Máxima Necesidad de Capital", f"${maxima_necesidad_capital:,.2f}", help="El punto más bajo del flujo de caja. Indica la máxima cantidad de dinero que el proyecto necesitará.")

st.header("Visualizaciones Principales")
v1, v2 = st.columns(2)

with v1:
    st.subheader("Desglose de Costos")
    costos_data = {
        'Categoría': ['Terreno', 'Urbanización', 'Construcción', 'Admin/Permisos'],
        'Monto': [costo_terreno, costo_urbanizacion, costo_total_construccion, gastos_admin_permisos]
    }
    costos_df = pd.DataFrame(costos_data)
    fig_pie = px.pie(costos_df, values='Monto', names='Categoría', hole=.3)
    st.plotly_chart(fig_pie, use_container_width=True)

with v2:
    st.subheader("Flujo de Caja Acumulado")
    fig_area = px.area(
        flujo_df,
        x=flujo_df.index,
        y='Flujo Acumulado',
    )
    fig_area.update_layout(xaxis_title='Mes del Proyecto', yaxis_title='Capital Acumulado ($)')
    st.plotly_chart(fig_area, use_container_width=True)


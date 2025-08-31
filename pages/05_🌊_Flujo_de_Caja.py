import streamlit as st
import pandas as pd
import numpy as np
import numpy_financial as npf
import plotly.express as px

st.set_page_config(layout="wide")
st.title("🌊 Flujo de Caja Proyectado")
st.markdown("Visualiza las entradas y salidas de dinero a lo largo del tiempo para entender la viabilidad y las necesidades de capital de tu proyecto.")

# --- Obtener todos los datos de st.session_state ---
cantidad_viviendas = st.session_state.get('cantidad_viviendas', 10)
precio_venta_unitario = st.session_state.get('precio_venta_unitario', 85000.0)
costo_terreno = st.session_state.get('costo_terreno', 100000.0)
costo_urbanizacion = st.session_state.get('total_urbanizacion', 84650.0)
costo_total_construccion = st.session_state.get('total_construccion_unitaria', 25850.0) * cantidad_viviendas
gastos_admin_permisos = st.session_state.get('total_gastos_admin_permisos', 90100.0)
monto_prestamo = st.session_state.get('monto_prestamo', 200000.0)
tasa_interes_anual = st.session_state.get('tasa_interes_anual', 5.0)
plazo_prestamo_anios = st.session_state.get('plazo_prestamo_anios', 15)


# --- Parámetros del Cronograma (Inputs del Usuario) ---
st.sidebar.header("Cronograma del Proyecto (en meses)")
duracion_total_meses = st.sidebar.slider("Duración Total del Proyecto (Meses)", 12, 60, 36)

st.sidebar.subheader("Fase de Inversión y Construcción")
mes_compra_terreno = st.sidebar.number_input("Mes de Compra del Terreno", 1, duracion_total_meses, 1)
mes_inicio_urbanizacion = st.sidebar.number_input("Mes Inicio Urbanización", 1, duracion_total_meses, 2)
mes_fin_urbanizacion = st.sidebar.number_input("Mes Fin Urbanización", 1, duracion_total_meses, 6)
mes_inicio_construccion = st.sidebar.number_input("Mes Inicio Construcción", 1, duracion_total_meses, 7)
mes_fin_construccion = st.sidebar.number_input("Mes Fin Construcción", 1, duracion_total_meses, 24)
mes_gastos_admin = st.sidebar.number_input("Mes de Gastos Admin/Permisos", 1, duracion_total_meses, 3)

st.sidebar.subheader("Fase de Ingresos y Financiamiento")
mes_recibo_prestamo = st.sidebar.number_input("Mes de Recepción del Préstamo", 1, duracion_total_meses, 2)
mes_inicio_ventas = st.sidebar.number_input("Mes Inicio de Ventas", 1, duracion_total_meses, 18)
mes_fin_ventas = st.sidebar.number_input("Mes Fin de Ventas", 1, duracion_total_meses, 36)
mes_inicio_pago_prestamo = st.sidebar.number_input("Mes Inicio Pago Préstamo", 1, duracion_total_meses, 3, help="Generalmente es un mes después de recibir el préstamo.")

# --- Construcción del DataFrame del Flujo de Caja ---
meses = np.arange(1, duracion_total_meses + 1)
flujo_df = pd.DataFrame(index=meses)

# Inicializar columnas en cero
flujo_df['Ingresos por Ventas'] = 0.0
flujo_df['Ingreso Préstamo'] = 0.0
flujo_df['Costo Terreno'] = 0.0
flujo_df['Costo Urbanización'] = 0.0
flujo_df['Costo Construcción'] = 0.0
flujo_df['Gastos Admin/Permisos'] = 0.0
flujo_df['Pago Préstamo'] = 0.0

# --- Distribuir los flujos en el tiempo ---

# ENTRADAS
flujo_df.loc[mes_recibo_prestamo, 'Ingreso Préstamo'] = monto_prestamo

duracion_ventas = mes_fin_ventas - mes_inicio_ventas + 1
if duracion_ventas > 0:
    ingreso_mensual_ventas = (precio_venta_unitario * cantidad_viviendas) / duracion_ventas
    flujo_df.loc[mes_inicio_ventas:mes_fin_ventas, 'Ingresos por Ventas'] = ingreso_mensual_ventas

# SALIDAS
flujo_df.loc[mes_compra_terreno, 'Costo Terreno'] = -costo_terreno
flujo_df.loc[mes_gastos_admin, 'Gastos Admin/Permisos'] = -gastos_admin_permisos

duracion_urbanizacion = mes_fin_urbanizacion - mes_inicio_urbanizacion + 1
if duracion_urbanizacion > 0:
    costo_mensual_urbanizacion = costo_urbanizacion / duracion_urbanizacion
    flujo_df.loc[mes_inicio_urbanizacion:mes_fin_urbanizacion, 'Costo Urbanización'] = -costo_mensual_urbanizacion

duracion_construccion = mes_fin_construccion - mes_inicio_construccion + 1
if duracion_construccion > 0:
    costo_mensual_construccion = costo_total_construccion / duracion_construccion
    flujo_df.loc[mes_inicio_construccion:mes_fin_construccion, 'Costo Construcción'] = -costo_mensual_construccion

# PAGO DEL PRÉSTAMO
if monto_prestamo > 0 and tasa_interes_anual > 0:
    tasa_mensual = (tasa_interes_anual / 100) / 12
    n_pagos = plazo_prestamo_anios * 12
    pago_mensual = -npf.pmt(tasa_mensual, n_pagos, monto_prestamo)
    
    # Aplicar el pago desde el mes de inicio hasta el final del proyecto o del préstamo
    mes_fin_pago_prestamo = min(duracion_total_meses, mes_inicio_pago_prestamo + n_pagos -1)
    flujo_df.loc[mes_inicio_pago_prestamo:mes_fin_pago_prestamo, 'Pago Préstamo'] = -pago_mensual


# --- Calcular Flujo Neto y Acumulado ---
flujo_df['Flujo Neto Mensual'] = flujo_df.sum(axis=1)
flujo_df['Flujo Acumulado'] = flujo_df['Flujo Neto Mensual'].cumsum()


# --- Visualización ---
st.header("Flujo de Caja Acumulado")
st.markdown("Este gráfico es crucial. Muestra cuánto dinero necesitas en total en cada punto del proyecto. El punto más bajo representa tu **máxima necesidad de financiamiento**.")

fig = px.area(
    flujo_df,
    x=flujo_df.index,
    y='Flujo Acumulado',
    title='Flujo de Caja Acumulado a lo Largo del Proyecto'
)
fig.update_layout(xaxis_title='Mes del Proyecto', yaxis_title='Capital Acumulado ($)')
st.plotly_chart(fig, use_container_width=True)

punto_minimo = flujo_df['Flujo Acumulado'].min()
st.metric("Máxima Necesidad de Capital (Punto más bajo del flujo)", f"${punto_minimo:,.2f}")


st.header("Tabla Detallada del Flujo de Caja Mensual")
st.dataframe(flujo_df.style.format("${:,.2f}").applymap(
    lambda v: 'color: red;' if v < 0 else ('color: green;' if v > 0 else 'color: black;'),
    subset=pd.IndexSlice[:, flujo_df.columns]
), use_container_width=True)

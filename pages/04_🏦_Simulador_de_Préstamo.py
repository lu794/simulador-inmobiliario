import streamlit as st
import pandas as pd
import numpy_financial as npf
import plotly.graph_objects as go

st.title("🏦 Simulador de Préstamo Bancario")
st.markdown("Calcula la cuota mensual y visualiza la tabla de amortización completa de tu financiamiento.")

# --- Función para calcular la tabla de amortización ---
def calcular_amortizacion(monto, tasa_anual, anios):
    if tasa_anual > 0:
        tasa_mensual = (tasa_anual / 100) / 12
        n_pagos = anios * 12
        pago_mensual = -npf.pmt(tasa_mensual, n_pagos, monto)
    else: # Si la tasa es 0, el cálculo es más simple
        tasa_mensual = 0
        n_pagos = anios * 12
        pago_mensual = monto / n_pagos if n_pagos > 0 else 0

    saldo_restante = monto
    data = []
    for i in range(1, n_pagos + 1):
        interes_pagado = saldo_restante * tasa_mensual
        capital_pagado = pago_mensual - interes_pagado
        saldo_restante -= capital_pagado
        
        # Asegurarse de que el saldo final sea exactamente 0
        if i == n_pagos:
            capital_pagado += saldo_restante
            saldo_restante = 0

        data.append({
            "Mes": i,
            "Cuota Mensual": pago_mensual,
            "Capital Pagado": capital_pagado,
            "Interés Pagado": interes_pagado,
            "Saldo Restante": saldo_restante
        })
    
    return pd.DataFrame(data), pago_mensual

# --- Entradas del Simulador ---
st.header("Parámetros del Préstamo")

# Usar valores de la página principal como defaults si existen
default_monto = st.session_state.get('monto_prestamo', 200000.0)
default_tasa = st.session_state.get('tasa_interes_anual', 5.0)
default_anios = st.session_state.get('plazo_prestamo_anios', 15)

col1, col2, col3 = st.columns(3)
with col1:
    monto_prestamo = st.number_input("Monto del Préstamo ($)", min_value=0.0, value=default_monto, step=1000.0)
with col2:
    tasa_interes_anual = st.number_input("Tasa de Interés Anual (%)", min_value=0.0, value=default_tasa, step=0.1)
with col3:
    plazo_prestamo_anios = st.number_input("Plazo del Préstamo (años)", min_value=1, value=default_anios, step=1)

# --- Cálculos y Visualización ---
if monto_prestamo > 0 and plazo_prestamo_anios > 0:
    tabla_amortizacion_df, pago_mensual = calcular_amortizacion(monto_prestamo, tasa_interes_anual, plazo_prestamo_anios)
    
    total_pagado = tabla_amortizacion_df['Cuota Mensual'].sum()
    total_intereses = tabla_amortizacion_df['Interés Pagado'].sum()

    st.header("Resumen del Financiamiento")
    res1, res2, res3 = st.columns(3)
    res1.metric("Cuota Mensual", f"${pago_mensual:,.2f}")
    res2.metric("Total Pagado", f"${total_pagado:,.2f}")
    res3.metric("Total Intereses Pagados", f"${total_intereses:,.2f}", help="Este es el costo total del financiamiento.")

    # --- Gráfico de Amortización ---
    st.subheader("Composición de Pagos a lo Largo del Tiempo")
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=tabla_amortizacion_df['Mes'],
        y=tabla_amortizacion_df['Capital Pagado'],
        name='Capital',
        marker_color='blue'
    ))
    fig.add_trace(go.Bar(
        x=tabla_amortizacion_df['Mes'],
        y=tabla_amortizacion_df['Interés Pagado'],
        name='Interés',
        marker_color='red'
    ))

    fig.update_layout(
        barmode='stack',
        title_text='Distribución de Capital e Interés por Mes',
        xaxis_title='Mes',
        yaxis_title='Monto Pagado ($)'
    )
    st.plotly_chart(fig, use_container_width=True)

    # --- Tabla de Amortización Detallada ---
    st.subheader("Tabla de Amortización Completa")
    st.dataframe(tabla_amortizacion_df.style.format({
        "Cuota Mensual": "${:,.2f}",
        "Capital Pagado": "${:,.2f}",
        "Interés Pagado": "${:,.2f}",
        "Saldo Restante": "${:,.2f}"
    }), use_container_width=True)

else:
    st.info("Introduce los detalles del préstamo para ver el análisis.")


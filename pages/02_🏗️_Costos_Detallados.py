import streamlit as st
import pandas as pd

st.set_page_config(page_title="Costos Detallados", page_icon="🏗️", layout="wide")
st.title("🏗️ Costos Detallados del Proyecto")
st.markdown("Desglosa los costos de urbanización (pagos únicos) y los costos de construcción por cada vivienda.")

# --- Inicializar DataFrames en st.session_state si no existen ---
if 'costos_urbanizacion_df' not in st.session_state:
    data_urbanizacion = {
        'Concepto': ['Movimiento de tierras', 'Red de alcantarillado', 'Red eléctrica', 'Pavimentación', 'Estudios y diseños'],
        'Valor Estimado': [15000.0, 25000.0, 18500.0, 22000.0, 4150.0]
    }
    st.session_state.costos_urbanizacion_df = pd.DataFrame(data_urbanizacion)

if 'costos_construccion_df' not in st.session_state:
    data_construccion = {
        'Componente': ['Cimentación', 'Estructura', 'Mampostería', 'Acabados', 'Instalaciones (agua, luz)'],
        'Costo por Vivienda': [5500.0, 7000.0, 4200.0, 6500.0, 2650.0]
    }
    st.session_state.costos_construccion_df = pd.DataFrame(data_construccion)


# --- Sección de Costos de Urbanización (Pago Único) ---
st.subheader("Costos de Urbanización (Total del Proyecto)")
edited_urbanizacion_df = st.data_editor(
    st.session_state.costos_urbanizacion_df,
    num_rows="dynamic",
    use_container_width=True,
    key="editor_urbanizacion"
)
st.session_state.costos_urbanizacion_df = edited_urbanizacion_df
total_urbanizacion = st.session_state.costos_urbanizacion_df['Valor Estimado'].sum()


# --- Sección de Costos de Construcción (Por Vivienda) ---
st.subheader("Costos de Construcción (Por Vivienda)")
edited_construccion_df = st.data_editor(
    st.session_state.costos_construccion_df,
    num_rows="dynamic",
    use_container_width=True,
    key="editor_construccion"
)
st.session_state.costos_construccion_df = edited_construccion_df
total_construccion_unitaria = st.session_state.costos_construccion_df['Costo por Vivienda'].sum()


# --- Resumen y Almacenamiento en st.session_state ---
st.subheader("Resumen de Costos")

col1, col2 = st.columns(2)
col1.metric("Total Costos de Urbanización", f"${total_urbanizacion:,.2f}")
col2.metric("Costo de Construcción por Vivienda", f",.2f")

# Guardar los totales para que la página principal los use
st.session_state.total_urbanizacion = total_urbanizacion
st.session_state.total_construccion_unitaria = total_construccion_unitaria

st.success("¡Costos actualizados! Los totales se han enviado a la página de 'Resumen del Proyecto'.")

if 'cantidad_viviendas' in st.session_state and st.session_state.cantidad_viviendas > 0:
    costo_total_construccion = total_construccion_unitaria * st.session_state.cantidad_viviendas
    st.info(f"El costo total de construcción para **{st.session_state.cantidad_viviendas} viviendas** es de **,.2f**.")

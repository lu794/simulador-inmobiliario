import streamlit as st
import pandas as pd

# No se llama a st.set_page_config() en las páginas secundarias.
st.title("🏗️ Detalle de Costos del Proyecto")
st.markdown("Introduce los costos directos de urbanización y construcción. Puedes añadir, editar o eliminar filas. Los totales se calcularán automáticamente y se usarán en la página de 'Resumen del Proyecto'.")

# --- Inicializar el estado de la sesión para guardar los datos ---
# NOTA: Es normal que tu editor de código subraye 'st.session_state' como un error.
# ¡Ignóralo! Es una característica de Streamlit y funcionará correctamente al ejecutar.
if 'costos_urbanizacion_df' not in st.session_state:
    # Datos de ejemplo basados en tu descripción
    data_urbanizacion = {
        'Concepto': ['Agua potable', 'Aguas negras', 'Energía eléctrica', 'Apertura de calles', 'Pavimento interno', 'Muro perimetral'],
        'Unidad': ['Global', 'Global', 'Global', 'm²', 'm²', 'm'],
        'Cantidad': [1.0, 1.0, 1.0, 1500.0, 1200.0, 300.0],
        'Precio Unitario': [15000.0, 12000.0, 25000.0, 8.50, 22.0, 45.0],
    }
    df = pd.DataFrame(data_urbanizacion)
    df['Costo Total'] = df['Cantidad'] * df['Precio Unitario']
    st.session_state.costos_urbanizacion_df = df

if 'costos_construccion_df' not in st.session_state:
    # Datos de ejemplo para la construcción de una vivienda tipo
    data_construccion = {
        'Partida': ['Preliminares', 'Cimentación', 'Estructura', 'Paredes', 'Techo', 'Acabados'],
        'Unidad': ['m²', 'm³', 'Global', 'm²', 'm²', 'm²'],
        'Cantidad': [100.0, 15.0, 1.0, 180.0, 110.0, 100.0],
        'Precio Unitario': [12.0, 150.0, 8000.0, 25.0, 35.0, 60.0],
    }
    df = pd.DataFrame(data_construccion)
    df['Costo Total'] = df['Cantidad'] * df['Precio Unitario']
    st.session_state.costos_construccion_df = df


# --- Tablas Interactivas para Costos ---

st.subheader("Detalle de Costos de Urbanización")
# st.data_editor crea una tabla editable tipo Excel
edited_urbanizacion_df = st.data_editor(
    st.session_state.costos_urbanizacion_df,
    num_rows="dynamic", # Permite al usuario añadir y borrar filas
    use_container_width=True,
    key="editor_urbanizacion", # Añadir una clave única ayuda a evitar errores
    column_config={
        "Costo Total": st.column_config.NumberColumn(
            "Costo Total ($)",
            help="Se calcula automáticamente (Cantidad * Precio Unitario)",
            disabled=True, # La columna no se puede editar manualmente
            format="$ {:,.2f}",
        ),
        "Precio Unitario": st.column_config.NumberColumn(format="$ %.2f"),
    }
)
# Recalcular el total si se edita la tabla y guardar los cambios en el estado de la sesión
if edited_urbanizacion_df is not None:
    edited_urbanizacion_df['Costo Total'] = edited_urbanizacion_df['Cantidad'] * edited_urbanizacion_df['Precio Unitario']
    st.session_state.costos_urbanizacion_df = edited_urbanizacion_df


st.subheader("Estructura de Costo de Construcción de Vivienda (por unidad)")
edited_construccion_df = st.data_editor(
    st.session_state.costos_construccion_df,
    num_rows="dynamic",
    use_container_width=True,
    key="editor_construccion", # Añadir una clave única ayuda a evitar errores
    column_config={
        "Costo Total": st.column_config.NumberColumn(
            "Costo Total ($)",
            help="Se calcula automáticamente (Cantidad * Precio Unitario)",
            disabled=True,
            format="$ {:,.2f}",
        ),
        "Precio Unitario": st.column_config.NumberColumn(format="$ %.2f"),
    }
)
# Recalcular el total y guardar cambios
if edited_construccion_df is not None:
    edited_construccion_df['Costo Total'] = edited_construccion_df['Cantidad'] * edited_construccion_df['Precio Unitario']
    st.session_state.costos_construccion_df = edited_construccion_df


# --- Cálculos y almacenamiento en el estado de la sesión ---
total_urbanizacion = st.session_state.costos_urbanizacion_df['Costo Total'].sum()
total_construccion_unitaria = st.session_state.costos_construccion_df['Costo Total'].sum()

st.subheader("Totales de Costos Directos")
col1, col2 = st.columns(2)
col1.metric("Costo Total de Urbanización", f"${total_urbanizacion:,.2f}")
col2.metric("Costo de Construcción por Vivienda", f"${total_construccion_unitaria:,.2f}")

# Guardar los totales para que la página principal pueda usarlos
st.session_state.total_urbanizacion = total_urbanizacion
st.session_state.total_construccion_unitaria = total_construccion_unitaria

st.success("¡Costos actualizados! Vuelve a la página 'Resumen del Proyecto' para ver el impacto en el análisis financiero.")
You can now view your Streamlit app in your browser.

Local URL: http://localhost:8501
Network URL: http://...

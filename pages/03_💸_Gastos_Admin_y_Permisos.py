import streamlit as st
import pandas as pd

st.title("💸 Gastos Administrativos y Permisos")
st.markdown("Aquí puedes desglosar los gastos operativos, administrativos, de activos y permisos. Los totales se reflejarán en el resumen del proyecto.")

# --- Inicializar DataFrames en st.session_state si no existen ---
if 'gastos_admin_df' not in st.session_state:
    data_admin = {
        'Concepto': ['Alquiler de oficina', 'Servicios públicos (luz, agua)', 'Sueldos y Salarios', 'Publicidad', 'Contabilidad externa'],
        'Valor Mensual': [500.0, 150.0, 3000.0, 200.0, 250.0]
    }
    st.session_state.gastos_admin_df = pd.DataFrame(data_admin)

if 'activos_df' not in st.session_state:
    data_activos = {
        'Activo Fijo': ['Laptop', 'Escritorio', 'Silla de oficina', 'Impresora'],
        'Cantidad': [2, 2, 2, 1],
        'Valor Unitario': [1200.0, 150.0, 75.0, 300.0]
    }
    st.session_state.activos_df = pd.DataFrame(data_activos)

if 'permisos_df' not in st.session_state:
    data_permisos = {
        'Permiso o Impuesto': ['Licencia ambiental', 'Permiso de urbanización', 'Permisos de construcción', 'Apertura de empresa'],
        'Valor Estimado': [3000.0, 5000.0, 4500.0, 1000.0]
    }
    st.session_state.permisos_df = pd.DataFrame(data_permisos)


# --- Sección de Gastos Administrativos (Mensuales) ---
st.subheader("Gastos Administrativos Recurrentes")
duracion_proyecto_meses = st.number_input("Duración estimada del proyecto (meses)", min_value=1, value=18, step=1, help="Meses durante los cuales se pagarán estos gastos.")
edited_admin_df = st.data_editor(
    st.session_state.gastos_admin_df,
    num_rows="dynamic",
    use_container_width=True,
    key="editor_admin"
)
st.session_state.gastos_admin_df = edited_admin_df
total_gastos_mensuales = st.session_state.gastos_admin_df['Valor Mensual'].sum()
total_admin_periodo = total_gastos_mensuales * duracion_proyecto_meses


# --- Sección de Activos Fijos (Pago Único) ---
st.subheader("Inversión en Activos Fijos")
edited_activos_df = st.data_editor(
    st.session_state.activos_df,
    num_rows="dynamic",
    use_container_width=True,
    key="editor_activos",
    column_config={
        "Valor Total": st.column_config.NumberColumn(
            "Valor Total ($)", disabled=True, format="$ {:,.2f}"
        )
    }
)
edited_activos_df['Valor Total'] = edited_activos_df['Cantidad'] * edited_activos_df['Valor Unitario']
st.session_state.activos_df = edited_activos_df
total_activos = st.session_state.activos_df['Valor Total'].sum()


# --- Sección de Permisos e Impuestos (Pago Único) ---
st.subheader("Impuestos y Permisos")
edited_permisos_df = st.data_editor(
    st.session_state.permisos_df,
    num_rows="dynamic",
    use_container_width=True,
    key="editor_permisos"
)
st.session_state.permisos_df = edited_permisos_df
total_permisos = st.session_state.permisos_df['Valor Estimado'].sum()


# --- Resumen y Almacenamiento en st.session_state ---
st.subheader("Resumen General de Gastos")
total_general_gastos_admin = total_admin_periodo + total_activos + total_permisos

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Admin (Proyecto)", f"${total_admin_periodo:,.2f}")
col2.metric("Total Activos", f"${total_activos:,.2f}")
col3.metric("Total Permisos", f"${total_permisos:,.2f}")
col4.metric("GRAN TOTAL", f"${total_general_gastos_admin:,.2f}")

# Guardar el gran total para que la página principal lo use
st.session_state.total_gastos_admin_permisos = total_general_gastos_admin

st.success("¡Gastos actualizados! El total se ha enviado a la página de 'Resumen del Proyecto'.")

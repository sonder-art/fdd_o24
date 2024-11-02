import streamlit as st
import requests
import pandas as pd

# Configuración de la página
st.title("Frontend con Streamlit")

# Cargar archivo CSV
uploaded_file = st.file_uploader("Sube un archivo CSV", type="csv")

if uploaded_file:
    # Leer y mostrar los datos cargados
    df = pd.read_csv(uploaded_file)
    st.write("Datos cargados:")
    st.write(df)

    # Obtener nombres de columnas
    columns = df.columns.tolist()

    # Seleccionar columna para la operación y tipo de operación
    column = st.selectbox("Selecciona una columna para la operación:", columns)
    operation = st.selectbox("Selecciona una operación:", ["mean", "max", "var"])

    # Botón para ejecutar la operación
    if st.button("Ejecutar operación"):
        # Realizar la solicitud al backend
        response = requests.post(
            "http://backend:8000/operation/",
            json={"column": column, "operation": operation}
        )

        # Mostrar el resultado
        if response.status_code == 200:
            result = response.json()["result"]
            st.write(f"Resultado de {operation} en la columna {column}: {result}")
        else:
            st.write("Error en la solicitud al backend.")


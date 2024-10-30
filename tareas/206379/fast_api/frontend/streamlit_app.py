import streamlit as st
import pandas as pd
import requests
import plotly.express as px
import plotly.graph_objects as go
from io import StringIO

# Configuración de la página
st.set_page_config(page_title="Análisis de Vinos", page_icon="🍷", layout="wide")
API_URL = "http://localhost:8000"

# Título principal
st.title("🍷 Análisis y Predicción de Calidad de Vinos")

# Sidebar para navegación
page = st.sidebar.selectbox(
    "Selecciona una página",
    ["Cargar Datos", "Visualización", "Predicción", "Elimina Datos"]
)

# Función para cargar datos desde CSV
def load_csv_data(file):
    # Leer el CSV
    df = pd.read_csv(file, sep=";")
    
    # Mapeo de nombres de columnas
    column_mapping = {
        'fixed acidity': 'fixed_acidity',
        'volatile acidity': 'volatile_acidity',
        'citric acid': 'citric_acid',
        'residual sugar': 'residual_sugar',
        'free sulfur dioxide': 'free_sulfur_dioxide',
        'total sulfur dioxide': 'total_sulfur_dioxide',
        'chlorides': 'chlorides',
        'density': 'density',
        'pH': 'pH',
        'sulphates': 'sulphates',
        'alcohol': 'alcohol',
        'quality': 'quality'
    }
    
    # Renombrar las columnas
    df = df.rename(columns=column_mapping)
    
    # Enviar cada fila a la API
    for _, row in df.iterrows():
        wine_data = row.to_dict()
        response = requests.post(f"{API_URL}/wines/", json=wine_data)
        if response.status_code != 200:
            st.error(f"Error al cargar fila: {response.text}")
            continue
    
    return df

if page == "Cargar Datos":
    st.header("Cargar Datos de Vinos")
    
    uploaded_file = st.file_uploader("Elige un archivo CSV", type="csv")
    if uploaded_file is not None:
        df = load_csv_data(uploaded_file)
        st.success(f"Datos cargados exitosamente: {len(df)} registros")
        st.dataframe(df)
    else:
        tot_response = requests.get(f"{API_URL}/wines/count")
        response = requests.get(f"{API_URL}/wines/")
        if response.status_code == 200:
            wines = response.json()
            if tot_response.json()['total'] >0:
                st.dataframe(wines)
            else:
                st.warning("No hay datos actualmente, porfavor cargalos")


elif page == "Visualización":
    st.header("Visualización de Datos")
    response = requests.get(f"{API_URL}/wines/")
    if response.status_code == 200:
        wines = response.json()
        df = pd.DataFrame(wines)
    # Obtener estadísticas
        response = requests.get(f"{API_URL}/wines/columns")
        if response.status_code == 200:
            column_list = response.json()['columns']
            selected_column = st.sidebar.selectbox("Selecciona una columna: ", column_list)
            
            # Obtener los datos de los vinos
            response = requests.post(f"{API_URL}/wines/columns", json={"column_name": selected_column})
            if response.status_code == 200:
                available_operations = response.json()['available_operations']
                selected_operation = st.sidebar.selectbox("Operaciones disponibles para dicha columna: ", available_operations)
                # Generar visualización de la columna seleccionada
                st.subheader(f"Distribución de {selected_column}")
                try:
                    # Usa getattr para obtener la función y luego llámala en la columna deseada
                    result = getattr(df[selected_column], selected_operation)()
                    st.write(f"El resultado de {selected_operation} en la columna {selected_column} es: {result}")
                except AttributeError:
                    st.error(f"La operación '{selected_operation}' no es válida para la columna seleccionada.")
                
        else:
            st.error("Error al obtener las columnas de los datos")


elif page == "Predicción":
    st.header("Predicción de Calidad")
    
    # Crear formulario para input
    with st.form("prediction_form"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            fixed_acidity = st.number_input("Fixed Acidity", value=7.0)
            volatile_acidity = st.number_input("Volatile Acidity", value=0.3)
            citric_acid = st.number_input("Citric Acid", value=0.3)
            residual_sugar = st.number_input("Residual Sugar", value=2.0)
        
        with col2:
            chlorides = st.number_input("Chlorides", value=0.08)
            free_sulfur_dioxide = st.number_input("Free Sulfur Dioxide", value=15.0)
            total_sulfur_dioxide = st.number_input("Total Sulfur Dioxide", value=100.0)
            density = st.number_input("Density", value=0.996)
        
        with col3:
            pH = st.number_input("pH", value=3.2)
            sulphates = st.number_input("Sulphates", value=0.5)
            alcohol = st.number_input("Alcohol", value=10.0)
            quality = st.number_input("Quality (para registro)", value=6, step=1)
        
        submitted = st.form_submit_button("Predecir Calidad")
        
        if submitted:
            # Crear objeto para predicción
            wine_data = {
                "fixed_acidity": fixed_acidity,
                "volatile_acidity": volatile_acidity,
                "citric_acid": citric_acid,
                "residual_sugar": residual_sugar,
                "chlorides": chlorides,
                "free_sulfur_dioxide": free_sulfur_dioxide,
                "total_sulfur_dioxide": total_sulfur_dioxide,
                "density": density,
                "pH": pH,
                "sulphates": sulphates,
                "alcohol": alcohol,
                "quality": quality
            }
            
            # Hacer predicción
            response = requests.post(f"{API_URL}/wines/predict_quality", json=wine_data)
            
            if response.status_code == 200:
                prediction = response.json()
                st.success(f"Calidad predicha: {prediction['predicted_quality']}")
                
                # Guardar el vino en la base de datos
                requests.post(f"{API_URL}/wines/", json=wine_data)
                st.info("Datos guardados en la base de datos")
            else:
                st.error("Error al hacer la predicción")

elif page == "Elimina Datos":
    st.header("Gestionar Datos")
    
    # Obtener el conteo actual de vinos
    response = requests.get(f"{API_URL}/wines/count")
    if response.status_code == 200:
        total_wines = response.json()["total"]
        st.info(f"Actualmente hay {total_wines} vinos en la base de datos")
    
    # Sección para borrar un vino específico
    st.subheader("Borrar vino específico")
    
    # Obtener lista de vinos
    response = requests.get(f"{API_URL}/wines/")
    if response.status_code == 200:
        wines = response.json()
        if wines:
            # Crear un DataFrame para mostrar los vinos
            wines_df = pd.DataFrame(wines)
            st.dataframe(wines_df)
            
            wine_id = st.number_input("ID del vino a eliminar", min_value=1, step=1)
            if st.button("Eliminar vino seleccionado"):
                response = requests.delete(f"{API_URL}/wines/{wine_id}")
                if response.status_code == 200:
                    st.success(response.json()["message"])
                    st.rerun()
                elif response.status_code == 404:
                    st.error("Vino no encontrado")
                else:
                    st.error("Error al eliminar el vino")
    
    # Sección para borrar todos los datos
    st.subheader("Borrar todos los datos")
    
    if total_wines > 0:
        col1, col2 = st.columns(2)
        with col1:
            confirm_text = st.text_input("Escribe 'BORRAR' para confirmar la eliminación de todos los datos")
        with col2:
            if st.button("Borrar todos los datos", type="primary", disabled=(confirm_text != "BORRAR")):
                response = requests.delete(f"{API_URL}/wines/delete/all")
                if response.status_code == 200:
                    st.success(response.json()["message"])
                    st.rerun()
                else:
                    st.error("Error al eliminar los datos")
    else:
        st.warning("No hay datos para eliminar en la base de datos")
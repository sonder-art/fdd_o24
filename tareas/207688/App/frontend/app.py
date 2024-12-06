# frontend/app.py
import streamlit as st
import requests
import pandas as pd

API_URL = "http://backend:8000"

st.title("Aplicación de Datos de Vino")

operation = st.selectbox("Seleccione la operación", ["Visualizar", "Agregar", "Eliminar"])

if operation == "Visualizar":
    response = requests.get(f"{API_URL}/wines")
    data = response.json().get("data", [])
    if data:
        df = pd.DataFrame(data)
        st.dataframe(df)
    else:
        st.write("No se encontraron datos.")

elif operation == "Agregar":
    with st.form("Formulario de vino"):
        Class = st.number_input("Class", min_value=1, max_value=3)
        Alcohol = st.number_input("Alcohol")
        Malic_acid = st.number_input("Malic acid")
        Ash = st.number_input("Ash")
        Alcalinity_of_ash = st.number_input("Alcalinity of ash")
        Magnesium = st.number_input("Magnesium", min_value=0)
        Total_phenols = st.number_input("Total phenols")
        Flavanoids = st.number_input("Flavanoids")
        Nonflavanoid_phenols = st.number_input("Nonflavanoid phenols")
        Proanthocyanins = st.number_input("Proanthocyanins")
        Color_intensity = st.number_input("Color intensity")
        Hue = st.number_input("Hue")
        OD280_OD315 = st.number_input("OD280/OD315 of diluted wines")
        Proline = st.number_input("Proline", min_value=0)
        
        submitted = st.form_submit_button("Agregar Vino")
        if submitted:
            wine_data = {
                "Class": Class,
                "Alcohol": Alcohol,
                "Malic_acid": Malic_acid,
                "Ash": Ash,
                "Alcalinity_of_ash": Alcalinity_of_ash,
                "Magnesium": Magnesium,
                "Total_phenols": Total_phenols,
                "Flavanoids": Flavanoids,
                "Nonflavanoid_phenols": Nonflavanoid_phenols,
                "Proanthocyanins": Proanthocyanins,
                "Color_intensity": Color_intensity,
                "Hue": Hue,
                "OD280_OD315": OD280_OD315,
                "Proline": Proline
            }
            response = requests.post(f"{API_URL}/wines", json=wine_data)
            st.write(response.json())

elif operation == "Eliminar":
    wine_id = st.number_input("ID del vino a eliminar", min_value=1)
    if st.button("Eliminar Vino"):
        response = requests.delete(f"{API_URL}/wines", params={"wine_id": wine_id})
        st.write(response.json())

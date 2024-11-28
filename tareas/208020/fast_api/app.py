# app.py

import streamlit as st
import pandas as pd
import requests

st.title("Dataset Metrics Calculator")

# Input for the filename
filename = st.text_input("Enter the filename (including .csv):")

def load_csv_with_fallback(filepath):
    # Try multiple encodings to read the CSV
    encodings_to_try = ['utf-8', 'ISO-8859-1', 'latin1', 'cp1252']
    for encoding in encodings_to_try:
        try:
            return pd.read_csv(filepath, encoding=encoding)
        except Exception as e:
            st.write(f"Failed to read with encoding {encoding}: {e}")
    st.error("Failed to read CSV file with supported encodings.")
    return None

# Check if the user provided a filename
if filename:
    data = load_csv_with_fallback(filename)
    if data is not None:
        st.write(data)

        # Select the column to analyze
        column = st.selectbox("Select a column to analyze", data.columns)

        if st.button("Calculate Metrics"):
            response = requests.post("http://fastapi_backend:8000/metrics", json={"filename": filename, "column": column})

            if response.status_code == 200:
                metrics = response.json()
                st.write("Metrics:")
                st.json(metrics)
            else:
                st.error("Error calculating metrics: " + response.json().get("detail", "Unknown error"))

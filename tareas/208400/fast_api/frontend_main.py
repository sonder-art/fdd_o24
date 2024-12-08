# frontend_main.py

import streamlit as st
import requests

# Title
st.title("CSV Column Statistics Calculator")

# Fetch available columns from backend
columns_response = requests.get("http://backend:8000/columns/")

# Check if columns were successfully fetched
if columns_response.status_code == 200:
    columns = columns_response.json()

    # Column selection dropdown
    selected_column = st.selectbox("Select Column", columns)

    # Calculate and display stats for the selected column
    if st.button("Calculate Statistics"):
        response = requests.get(f"http://backend:8000/calculate-stats/{selected_column}")
        
        if response.status_code == 200:
            stats = response.json()

            # Display statistics in labeled text boxes
            st.write(f"Statistics for `{selected_column}`:")
            col1, col2 = st.columns(2)

            col1.text("Mean")
            col2.text(stats.get("mean"))

            col1.text("Median")
            col2.text(stats.get("median"))

            col1.text("Mode")
            col2.text(", ".join(map(str, stats.get("mode"))))  # Display as comma-separated values

            col1.text("Variance")
            col2.text(stats.get("variance"))

            col1.text("Standard Deviation")
            col2.text(stats.get("std_dev"))
            
        else:
            st.error("Error: Could not retrieve statistics.")
else:
    st.error("No numeric columns found in the CSV.")

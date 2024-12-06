# frontend/app.py
import streamlit as st
import requests
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Online Retail Analysis", layout="centered")

st.markdown(
    """
    <style>
        .title { font-size: 36px; font-weight: bold; color: #4CAF50; }
        .section-header { font-size: 24px; font-weight: bold; color: #FFC107; }
        .column-info, .table-container { background-color: #1c1c1c; padding: 10px; border-radius: 8px; }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Online Retail Analysis")

st.markdown("""
This application allows you to analyze the `online_retail.xlsx` dataset by displaying available columns and performing statistical and graphical calculations.
""")

# Section: Load Dataset and Show Head of Data
st.header("Dataset Preview")

# Fetch the first few rows of data
try:
    head_response = requests.get("http://backend:8000/head/")
    if head_response.status_code == 200:
        data_head = pd.DataFrame(head_response.json()["head"])
        st.write("### First 10 Rows of the Dataset")
        st.dataframe(data_head)
    else:
        st.error("Failed to load dataset preview. Please check the backend service.")
except requests.exceptions.RequestException:
    st.error("Could not connect to backend. Ensure the backend service is running.")

# Section: Column Information
st.header("Available Columns and Types")
try:
    # Fetch columns and types from backend
    response = requests.get("http://backend:8000/columns/")
    if response.status_code == 200:
        column_info = response.json()
        
        # Convert to DataFrame for display
        col_df = pd.DataFrame(list(column_info.items()), columns=["Column Name", "Type"])
        st.write("### Column Information")
        st.table(col_df)
    else:
        st.error("Failed to load dataset. Please check the backend service.")
except requests.exceptions.RequestException:
    st.error("Could not connect to backend. Ensure the backend service is running.")

# Section: Statistical Calculations and Graphing
st.header("Statistical Calculations and Graphing")

# Check if columns are loaded
if 'column_info' in locals() and column_info:
    column = st.selectbox("Choose a column", column_info.keys())

    # Only allow statistical operations for numeric columns
    if column_info[column] == "numeric":
        operation = st.selectbox("Choose a statistical operation", ["mean", "max", "min", "variance"])
        
        if st.button("Calculate"):
            try:
                calc_response = requests.get(f"http://backend:8000/calculate/?column={column}&operation={operation}")
                if calc_response.status_code == 200:
                    result = calc_response.json().get("result")
                    st.success(f"The {operation} of `{column}` is: {result}")
                else:
                    st.error("Calculation failed. Please ensure the column and operation are valid.")
            except requests.exceptions.RequestException:
                st.error("Could not connect to backend for calculation.")
    elif column_info[column] == "string":
        # Display options for string columns (like most frequent value)
        st.subheader("String Column Analysis")
        if st.button("Find Most Frequent Value"):
            try:
                freq_response = requests.get(f"http://backend:8000/most_frequent/?column={column}")
                if freq_response.status_code == 200:
                    result = freq_response.json().get("most_frequent")
                    st.success(f"The most frequent value in `{column}` is: {result}")
                else:
                    st.error("Failed to calculate the most frequent value.")
            except requests.exceptions.RequestException:
                st.error("Could not connect to backend for calculation.")
    else:
        st.warning("Statistical calculations are only available for numeric and string columns.")

    # Graphing section
    st.subheader("Graphing Options")
    graph_column = st.selectbox("Choose a column to graph", ["Quantity", "UnitPrice"])
    group_by = st.selectbox("Group by", ["None", "Country", "InvoiceDate"])

    if st.button("Generate Graph"):
        try:
            graph_response = requests.get(f"http://backend:8000/graph/?column={graph_column}&group_by={group_by}")
            if graph_response.status_code == 200:
                data = pd.DataFrame(graph_response.json()["data"])
                
                # Generate appropriate graph
                if group_by == "None":
                    fig = px.histogram(data, x=graph_column)
                else:
                    fig = px.bar(data, x=group_by, y=graph_column, title=f"{graph_column} by {group_by}")
                
                st.plotly_chart(fig)
            else:
                st.error("Failed to generate graph.")
        except requests.exceptions.RequestException:
            st.error("Could not connect to backend for graph generation.")
else:
    st.info("The dataset must be loaded successfully to view columns and perform calculations.")




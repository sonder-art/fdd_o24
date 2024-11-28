import streamlit as st
import pandas as pd
import requests

# Set up the Streamlit app title
st.title("CSV Data Analyzer")

# File uploader to upload a CSV file
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    # Load the CSV into a DataFrame
    df = pd.read_csv(uploaded_file, delimiter=";")
    
    # Display the first few rows to check the data
    st.write("First few rows of the dataset:")
    st.write(df.head())

    # Display the columns available in the CSV
    st.write("Columns in the dataset:")
    columns = df.columns.tolist()
    st.write(columns)

    # Select a column to analyze
    selected_column = st.selectbox("Select a column to analyze", columns)

    # Check if the selected column is numeric
    if pd.api.types.is_numeric_dtype(df[selected_column]):
        # Calculate and display statistics if it's numeric
        st.write(f"Statistics for '{selected_column}':")
        st.write(f"Max: {df[selected_column].max()}")
        st.write(f"Min: {df[selected_column].min()}")
        st.write(f"Median: {df[selected_column].median()}")
        st.write(f"Quantiles:")
        st.write(df[selected_column].quantile([0.25, 0.5, 0.75]))
    else:
        # Display a message if it's not numeric
        st.write(f"'{selected_column}' is not a numeric column.")

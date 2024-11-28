import streamlit as st
import requests
import pandas as pd

st.title("Obesity Data Analysis")

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
if uploaded_file is not None:
    st.write("File uploaded, sending to API for analysis...")

    # Send file to FastAPI
    files = {'file': uploaded_file.getvalue()}
    response = requests.post("http://backend:8000/analyze/", files=files)
    if response.status_code == 200:
        summary = response.json().get("summary")
        if summary:
            st.write("Summary Statistics:")
            st.write(pd.DataFrame(summary))
        else:
            st.write("No summary available.")
    else:
        st.write("Error in analysis.")

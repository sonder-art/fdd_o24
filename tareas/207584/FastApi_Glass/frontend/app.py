import pandas as pd
import streamlit as st
import requests

# Set FastAPI URL
fastapi_url = "http://backend:8000/analyze"

# Set the title and subtitle
st.title("Glass Composition Analysis")
st.write("This application displays the mean composition of various elements in glass samples.")

# Add a button to trigger the analysis
if st.button("Analyze Glass Samples"):
    # Call FastAPI to get analysis
    response = requests.get(fastapi_url)

    if response.status_code == 200:
        analysis = response.json()
        mean_values = analysis["mean_values"]

        # Display the results in a formatted table
        st.write("### Mean Composition of Elements")
        st.write("Here are the mean values for the composition of the glass samples:")

        # Create a DataFrame for better visualization
        mean_df = pd.DataFrame(mean_values.items(), columns=['Element', 'Mean Value'])
        st.table(mean_df)  # Display the DataFrame as a table

    else:
        st.error(f"Failed to retrieve data from backend. Status code: {response.status_code}")

# Add additional information
st.write("#### About This Application")
st.info("This application utilizes FastAPI to analyze glass compositions based on a dataset.")

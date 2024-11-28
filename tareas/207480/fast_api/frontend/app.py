#app.py frontend
import streamlit as st
import requests

# Configure the backend API URL
API_URL = "http://backend:8000/api/v1"

st.title("FastAPI + Streamlit Demo")

# ... rest of the code for creating a new item ...

# Statistics Section
st.header("Wine Data Statistics")

# Fetch the available columns from the backend
response = requests.get(f"{API_URL}/columns/")
if response.status_code == 200:
  columns = response.json()
else:
  st.error("Error fetching columns from the backend")
  columns = []

# Select a column to analyze
selected_column = st.selectbox("Select a column", columns)

if st.button("Get Statistics"):
  if selected_column:
    # Request statistics from the backend
    response = requests.get(f"{API_URL}/statistics/{selected_column}/")
    if response.status_code == 200:
      stats = response.json()
      st.write(f"**Mean:** {stats['mean']}")
      st.write(f"**Variance:** {stats['variance']}")
      st.write(f"**Standard Deviation:** {stats['std_dev']}")
    else:
      st.error("Error fetching statistics from the backend")
  else:
    st.warning("Please select a column")
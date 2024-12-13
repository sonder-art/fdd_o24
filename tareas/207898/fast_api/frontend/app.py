# frontend/app.py

import streamlit as st
import requests

st.title("Streamlit Frontend")

# Input form
with st.form("item_form"):
    name = st.text_input("Item Name")
    description = st.text_area("Description")
    price = st.number_input("Price", min_value=0.0)
    tax = st.number_input("Tax", min_value=0.0)
    submitted = st.form_submit_button("Submit")

if submitted:
    # Prepare the payload
    payload = {
        "name": name,
        "description": description,
        "price": price,
        "tax": tax
    }
    
    # Make a POST request to the FastAPI backend
    try:
        response = requests.post("http://backend:8000/items/", json=payload)
        if response.status_code == 200:
            st.success("Item created successfully!")
            st.json(response.json())
        else:
            st.error(f"Error: {response.status_code}")
    except requests.exceptions.RequestException as e:
        st.error(f"Request failed: {e}")

# Display a welcome message from the backend
st.header("Backend Message")
try:
    response = requests.get("http://backend:8000/")
    if response.status_code == 200:
        st.write(response.json()["message"])
    else:
        st.error(f"Error: {response.status_code}")
except requests.exceptions.RequestException as e:
    st.error(f"Request failed: {e}")

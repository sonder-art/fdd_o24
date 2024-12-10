import streamlit as st
import requests

st.title("Streamlit Frontend for FastAPI")

# Fetch data from FastAPI
response = requests.get("http://backend:80")  # Cambiar "localhost" por "backend"
if response.status_code == 200:
    data = response.json()
    st.write("Message from FastAPI:", data["message"])

# Form to create a new item
name = st.text_input("Item Name")
value = st.number_input("Value", min_value=0, step=1)
if st.button("Create Item"):
    item = {"name": name, "value": value}
    create_response = requests.post("http://backend:80/items/", json=item)
    if create_response.status_code == 200:
        st.write("Item created:", create_response.json())
    else:
        st.write("Failed to create item")

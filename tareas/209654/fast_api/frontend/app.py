import streamlit as st
import requests

backend_url = "http://backend:8000"

st.title("Word Array Manager")

# Input to add a word
word = st.text_input("Enter a word to add to the array")

if st.button("Add Word"):
    response = requests.post(f"{backend_url}/words/", json={"word": word})
    if response.status_code == 200:
        st.success(f"Added: {word}")
    else:
        st.error("Error adding word")
# Display current words
st.header("Current Words in Array")
words_response = requests.get(f"{backend_url}/words/")
if words_response.status_code == 200:
    words = words_response.json().get("words", [])
    st.write(words)
else:
    st.error("Failed to fetch words")


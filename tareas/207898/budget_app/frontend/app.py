import streamlit as st
import requests
import os
import pandas as pd

# Get the backend URL from the environment variable
BACKEND_URL = os.getenv("BACKEND_URL", "http://backend:8000")

st.title("Personal Budget App")

# Function to fetch transactions from the backend
def get_transactions():
    response = requests.get(f"{BACKEND_URL}/transactions/")
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Error fetching transactions.")
        return []

# Fetch transactions from the backend
transactions = get_transactions()

# Convert transactions to a DataFrame
if transactions:
    df = pd.DataFrame(transactions)

    # Calculate total balance
    df['amount'] = pd.to_numeric(df['amount'])
    total_balance = df.apply(lambda x: x['amount'] if x['category'] == 'Income' else -x['amount'], axis=1).sum()

    # Add a summary row for the total balance
    total_row = pd.DataFrame([{
        'date': 'Total',
        'description': '',
        'amount': total_balance,
        'category': 'Balance',
        'id': None
    }])

    # Append the total row to the DataFrame
    df = pd.concat([df, total_row], ignore_index=True)

    # Display the updated table without the ID column
    st.subheader("Transactions")
    for index, row in df.iterrows():
        cols = st.columns((3, 3, 2, 2, 1))
        cols[0].write(row['date'])
        cols[1].write(row['description'])
        cols[2].write(row['amount'])
        cols[3].write(row['category'])
        if row['date'] != 'Total':
            delete_button = cols[4].button("🗑️", key=f"delete_{row['id']}")
            if delete_button:
                # Delete transaction
                response = requests.delete(f"{BACKEND_URL}/transactions/{row['id']}")
                if response.status_code == 200:
                    st.success("Transaction deleted successfully!")
                    # JavaScript reload to refresh the page
                    st.markdown("<script>window.location.reload();</script>", unsafe_allow_html=True)
                else:
                    st.error("Error deleting transaction.")

else:
    st.subheader("Transactions")
    st.write("No transactions yet.")

# Form to add new transaction
st.subheader("Add New Transaction")
with st.form("transaction_form"):
    date = st.date_input("Date")
    description = st.text_input("Description")
    amount = st.number_input("Amount", step=0.01)
    category = st.selectbox("Category", ["Income", "Expense"])
    submitted = st.form_submit_button("Add Transaction")

    if submitted:
        transaction_data = {
            "date": str(date),
            "description": description,
            "amount": amount,
            "category": category
        }
        response = requests.post(f"{BACKEND_URL}/transactions/", json=transaction_data)
        if response.status_code == 200:
            st.success("Transaction added successfully!")
            # JavaScript reload to refresh the page
            st.markdown("<script>window.location.reload();</script>", unsafe_allow_html=True)
        else:
            st.error("Error adding transaction.")
import streamlit as st
from queries import *

st.title('Hae yrityksen tiedot')

# Fetch the company names for the selectbox
company_names = get_company_names()

# Use a placeholder for the company data to display it later
company_data_placeholder = st.empty()

# Create a selectbox for user to choose the company
selected_company = st.selectbox('Valitse yritys', company_names)

# Button to trigger the data fetching
if st.button('Hae tiedot'):
    # When the button is clicked, fetch and display the data for the selected company
    data = fetch_data3(selected_company)
    company_data_placeholder.write(data)

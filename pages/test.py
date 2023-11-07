import streamlit as st
from queries import *

st.title('Hae yrityksen tiedot')

# Fetch and display the selectbox with company names
company_names = get_company_names()
selected_company = st.selectbox('Valitse yritys', company_names)

# When a company is selected, fetch and display the data
if selected_company:
    data = fetch_data3(selected_company)
    st.write(data)


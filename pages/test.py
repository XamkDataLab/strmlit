import streamlit as st
from queries import *

st.title('Hae yrityksen tiedot')

company_names = get_company_names()
    selected_company = st.selectbox('Select a company', company_names)

f selected_company:
        data = fetch_data_by_company_name(selected_company)
        st.write(data)


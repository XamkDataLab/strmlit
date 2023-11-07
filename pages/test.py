import streamlit as st
from queries import get_company_names, fetch_data3

st.title('Hae yrityksen tiedot')

all_company_names = get_company_names()

search_query = st.text_input('Hae yritystä')

filtered_company_names = [name for name in all_company_names if search_query.lower() in name.lower()]

if search_query:
    selected_company = st.selectbox('Valitse yritys', filtered_company_names)
else:
    selected_company = st.selectbox('Valitse yritys', all_company_names[:50])  # Show only the first 50 names or some limited number

if st.button('Hae tiedot'):
    if selected_company:
        data = fetch_individual_data(selected_company)
        st.write(data)


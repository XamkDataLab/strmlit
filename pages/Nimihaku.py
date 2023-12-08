import streamlit as st
from queries import *

all_company_data = get_company_names2()

search_query = st.text_input('Hae yritystä')

# Filter company names based on the search query
filtered_company_names = all_company_data[all_company_data['yritys'].str.lower().str.contains(search_query.lower())]

if search_query:
    selected_company = st.selectbox('Valitse yritys', filtered_company_names['yritys'])
else:
    # Show only the first 50 names or some limited number
    selected_company = st.selectbox('Valitse yritys', all_company_data['yritys'][:50])

if st.button('Hae tiedot'):
    if selected_company:
        # Retrieve the y_tunnus for the selected company
        y_tunnus = filtered_company_names[filtered_company_names['yritys'] == selected_company]['y_tunnus'].iloc[0]
        data = fetch_individual_data(y_tunnus)
        st.write(data)



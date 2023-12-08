import streamlit as st
from queries import *

# Load company data
all_company_data = get_company_names2()

# Input for search query
search_query = st.text_input('Hae yritystä')

if search_query:
    # Filter company names based on the search query
    filtered_company_names = all_company_data[all_company_data['yritys'].str.lower().str.contains(search_query.lower())]
    dropdown_options = filtered_company_names['yritys']
else:
    # Show only the first 50 names or some limited number if no search query
    dropdown_options = all_company_data['yritys'][:50]

selected_company = st.selectbox('Valitse yritys', dropdown_options)

if st.button('Hae tiedot') and selected_company:
    # Check if the selected company is in the filtered list
    if selected_company in filtered_company_names['yritys'].values:
        # Retrieve the y_tunnus for the selected company
        y_tunnus = filtered_company_names[filtered_company_names['yritys'] == selected_company]['y_tunnus'].iloc[0]
        data = fetch_individual_data(y_tunnus)
        st.write(data)
    else:
        st.error("Valittua yritystä ei löytynyt.")



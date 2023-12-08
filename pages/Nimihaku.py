import streamlit as st
from queries import *

# Load company data with caching
@st.cache
def load_company_data():
    return get_company_names2()

all_company_data = load_company_data()

# Input for search query
search_query = st.text_input('Hae yritystä')

if search_query:
    filtered_company_names = all_company_data[all_company_data['yritys'].str.lower().str.contains(search_query.lower())]
    dropdown_options = filtered_company_names['yritys']
else:
    dropdown_options = all_company_data['yritys'][:50]  # Limiting the number of options

selected_company = st.selectbox('Valitse yritys', dropdown_options)

if st.button('Hae tiedot') and selected_company:
    try:
        # Fetch and display data for the selected company
        if selected_company in filtered_company_names['yritys'].values:
            y_tunnus = filtered_company_names[filtered_company_names['yritys'] == selected_company]['y_tunnus'].iloc[0]
            data = fetch_individual_data(y_tunnus)
            st.write(data)
        else:
            st.error("Valittua yritystä ei löytynyt.")
    except Exception as e:
        st.error(f"An error occurred: {e}")



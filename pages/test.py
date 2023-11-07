import streamlit as st
from queries import get_company_names, fetch_data3

st.title('Hae yrityksen tiedot')

# Fetch all company names
all_company_names = get_company_names()

# Text input for search query
search_query = st.text_input('Hae yritystä')

# Filter company names based on the search query
filtered_company_names = [name for name in all_company_names if search_query.lower() in name.lower()]

# If the search query is empty, don't display any options or display a limited number of companies
if search_query:
    selected_company = st.selectbox('Valitse yritys', filtered_company_names)
else:
    selected_company = st.selectbox('Valitse yritys', all_company_names[:50])  # Show only the first 50 names or some limited number

# Button to trigger the data fetching
if st.button('Hae tiedot'):
    # When the button is clicked, fetch and display the data for the selected company
    if selected_company:
        data = fetch_data3(selected_company)
        st.write(data)


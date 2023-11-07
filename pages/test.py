import streamlit as st
from queries import *

st.title('Hae yrityksen tiedot')

# Input for search
search_term = st.text_input("Anna Y-tunnus tai yrityksen nimi (ja paina enter)")
search_type = st.radio("Valitse hakutyyppi:", ('y_tunnus', 'company_name'))

if search_term:
  
    data = fetch_data_new(search_term, search_by=search_type)
    
    # Check if the data is not empty
    if not data.empty:
        st.write(f"Tulokset hakutermin '{search_term}' mukaan:")
        st.dataframe(data)  # Display the DataFrame in the app
    else:
        st.write("Ei tuloksia hakuehdoilla.")

import streamlit as st

st.title(f"Details for {y_tunnus}")
# detailed_info.py

import streamlit as st

def app():
    y_tunnus = st.session_state.get('y_tunnus', None)
    query_type = st.session_state.get('type', None)

    if y_tunnus and query_type:
        data = another_fetch_data_function(y_tunnus, query_type)
        
        if not data.empty:
            # Code to display data and visualization
            ...
        else:
            st.write("No data found.")


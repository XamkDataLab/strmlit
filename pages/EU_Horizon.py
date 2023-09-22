import streamlit as st
from queries import *

y_tunnus = st.session_state.get('y_tunnus')
st.title(f"EU Horizon funding for {y_tunnus}")

data = fetch_horizon_data(y_tunnus)
        if not data.empty:
            # Code to display data and visualization
            ...
        else:
            st.write("No data found.")
    else:
        st.write("Invalid or missing parameters.")



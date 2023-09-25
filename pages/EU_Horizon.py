import streamlit as st
from queries import *

yritys_basename = st.session_state.get('yritys_basename')
st.title(f"EU Horizon funding for {yritys_basename}")
st.write(f"Debug: yritys_basename = {yritys_basename}")

if yritys_basename:
    data = fetch_horizon_data(yritys_basename)
    if not data.empty:
        st.dataframe(data)
    else:
        st.write("No data found.")
else:
    st.write("Invalid or missing parameters.")



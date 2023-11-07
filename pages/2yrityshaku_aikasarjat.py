import streamlit as st
import pandas as pd
import plotly.express as px
import datetime
from queries import *

y_tunnus = st.session_state.get('y_tunnus')
st.title(f"Otsikko yritykselle {y_tunnus}")

if y_tunnus:
    data = fetch_company_data(y_tunnus)
else:
    st.write("Invalid or missing parameters.")
    
st.dataframe(data)


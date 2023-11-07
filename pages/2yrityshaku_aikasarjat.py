import streamlit as st
import pandas as pd
import plotly.express as px
import datetime
from queries import *


ytunnus = st.session_state.get('y_tunnus')
st.title(f"Otsikko yritykselle {y_tunnus}")

if ytunnus:
    data = fetch_individual_data(y_tunnus)
else:
    st.write("Invalid or missing parameters.")
    
st.DataFrame(data)


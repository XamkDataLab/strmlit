import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
from queries import *
st.title("Patents Expiring Soon")

df = fetch_legal_status_data()

option = st.selectbox('Show patents expiring in the next:', ['3 months', '6 months', '12 months'])

if option == '3 months':
    max_date = datetime.today() + timedelta(days=90)
elif option == '6 months':
    max_date = datetime.today() + timedelta(days=180)
else:
    max_date = datetime.today() + timedelta(days=365)

filtered_df = df[df['legal_status_anticipated_term_date'] <= max_date]

# Display the filtered data
st.write(f"Active Patents Expiring in the Next {option}:")
st.table(filtered_df[['lens_id', 'invention_title']])


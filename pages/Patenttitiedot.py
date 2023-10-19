import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
from queries import *


current_date = datetime.today().strftime('%Y-%m-%d')  
st.title(f"Yritysten erääntyviä patentteja {current_date}")

@st.cache(allow_output_mutation=True)
df = fetch_legal_status_data()
df['legal_status_anticipated_term_date'] = pd.to_datetime(df['legal_status_anticipated_term_date'])
df = df[df['legal_status_anticipated_term_date'].notna()]
st.write(df.head())

option = st.selectbox('Näytä patentit jotka eräänyvät', ['3 kuukauden kuluessa', '6 kuukauden kuluessa', '12 kuukauden kuluessa'])

# Set the minimum date as the current date
min_date = datetime.today()

if option == '3 months':
    max_date = min_date + timedelta(days=90)
elif option == '6 months':
    max_date = min_date + timedelta(days=180)
else:  # 12 months
    max_date = min_date + timedelta(days=365)

expiring_df = df[(df['legal_status_anticipated_term_date'] >= min_date) & (df['legal_status_anticipated_term_date'] <= max_date)]

unique_applicants = expiring_df['extracted_name'].dropna().unique().tolist()
selected_applicant = st.selectbox('Valitse hakija:', unique_applicants)

filtered_df = expiring_df[expiring_df['extracted_name'] == selected_applicant]

# Display the filtered data
st.write(f"Aktiiviset patentit hakijalta {selected_applicant} jotke erääntyvät seuraavan {option}:")
st.table(filtered_df[['lens_id', 'invention_title', 'yritys', 'extracted_name', 'legal_status_anticipated_term_date']])

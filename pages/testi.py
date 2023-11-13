import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from queries import *

def make_cpc(df, cpc_json_file):
    
    cpc = pd.read_json(cpc_json_file)
    df[['Section', 'Class', 'Subclass', 'Group', 'Subgroup']] = df['cpc_classification'].apply(breakdown_cpc)
    df['Group'] = df['Group'].apply(lambda x: x + "/00")
    df.drop(['cpc_code_split', 'class'], axis=1, inplace=True)
    df['Section Description'] = df['Section'].map(cpc.set_index('Code')['Description'])
    df['Class Description'] = df['Class'].map(cpc.set_index('Code')['Description'])
    df['Subclass Description'] = df['Subclass'].map(cpc.set_index('Code')['Description'])
    df['Group Description'] = df['Group'].map(cpc.set_index('Code')['Description'])
    df['Subgroup Description'] = df['Subgroup'].map(cpc.set_index('Code')['Description'])

    return df


y_tunnus = st.session_state.get('y_tunnus')
yritys_nimi = st.session_state.get('yritys')

if y_tunnus:
        cpc_data = fetch_company_cpc_data(y_tunnus)
  
        

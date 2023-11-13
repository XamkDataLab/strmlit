import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from queries import *
import plotly.express as px

json_url = "https://raw.githubusercontent.com/XamkDataLab/strmlit/main/cpc_ultimate_titles.json"

def breakdown_cpc(code):
    section = code[0]
    c_class = code[:3]
    subclass = code[:4]
    group = code.split('/')[0]
    subgroup = code
    return pd.Series([section, c_class, subclass, group, subgroup])

def make_cpc(df):
    
    cpc = pd.read_json(json_url)
    df[['Section', 'Class', 'Subclass', 'Group', 'Subgroup']] = df['cpc_classification'].apply(breakdown_cpc)
    df['Group'] = df['Group'].apply(lambda x: x + "/00")
    #df.drop(['cpc_code_split', 'class'], axis=1, inplace=True)
    df['Section Description'] = df['Section'].map(cpc.set_index('Code')['Description'])
    df['Class Description'] = df['Class'].map(cpc.set_index('Code')['Description'])
    df['Subclass Description'] = df['Subclass'].map(cpc.set_index('Code')['Description'])
    df['Group Description'] = df['Group'].map(cpc.set_index('Code')['Description'])
    df['Subgroup Description'] = df['Subgroup'].map(cpc.set_index('Code')['Description'])
    return df

def create_sunburst_chart(y_tunnus):
    cpc_data = fetch_company_cpc_data(y_tunnus)
    cpc_data = make_cpc(cpc_data)
    st.dataframe(cpc_data)

    # Grouping and counting for sunburst chart
    path = ['Section', 'Class', 'Subclass', 'Group', 'Subgroup']
    df_sunburst = cpc_data.groupby(path).size().reset_index(name='Counts')

    # Creating unique labels and parents for each level
    df_sunburst['Label'] = df_sunburst['Section'] + ' - ' + df_sunburst['Class'] + ' - ' + df_sunburst['Subclass'] + ' - ' + df_sunburst['Group'] + ' - ' + df_sunburst['Subgroup']
    df_sunburst['Parent'] = df_sunburst['Section'] + ' - ' + df_sunburst['Class'] + ' - ' + df_sunburst['Subclass'] + ' - ' + df_sunburst['Group']
    
    # Setting parents for the top level (Section) to ''
    df_sunburst.loc[df_sunburst['Class'] == df_sunburst['Section'], 'Parent'] = ''

    # Creating the sunburst chart
    fig = go.Figure(go.Sunburst(
        labels=df_sunburst['Label'],
        parents=df_sunburst['Parent'],
        values=df_sunburst['Counts'],
        branchvalues="total",
    ))

    fig.update_layout(margin=dict(t=0, l=0, r=0, b=0))

    st.plotly_chart(fig)

def create_treemap(df):
    fig = px.treemap(df, path=['Section', 'Class', 'Subclass', 'Group', 'Subgroup'],
                     values='Counts',
                     title="CPC Classification Treemap")
    st.plotly_chart(fig)
    
y_tunnus = st.session_state.get('y_tunnus')
yritys_nimi = st.session_state.get('yritys')

if y_tunnus:
    cpc_data = fetch_company_cpc_data(y_tunnus)
    cpc_data = make_cpc(cpc_data)
    create_treemap(cpc_data)



            

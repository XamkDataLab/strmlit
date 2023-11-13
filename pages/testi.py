import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from queries import *
import plotly.express as px
import graphviz as gv

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
    
def create_sunburst_chart(df):
    # Creating unique IDs by concatenating 'Group' and 'Subgroup'
    df['id'] = df['Group'] + '-' + df['Subgroup']
    df['parent'] = df['Group']
    df['label'] = df['Subgroup Description']

    # Handling NaN values by replacing them with a placeholder
    df.fillna('Unknown', inplace=True)

    # Adding root node
    root_df = pd.DataFrame({
        'id': ['root'],
        'parent': [None],
        'label': ['CPC Classifications']
    })
    df = pd.concat([root_df, df])

    # Creating the sunburst chart
    fig = go.Figure(go.Sunburst(
        ids=df['id'],
        labels=df['label'],
        parents=df['parent'],
        branchvalues="total"
    ))

    fig.update_layout(margin=dict(t=0, l=0, r=0, b=0))
    return fig


def create_test_sunburst_chart():
    # Hard-coded simple example
    fig = go.Figure(go.Sunburst(
        ids=["root", "A", "B", "AA", "AB", "BA", "BB"],
        labels=["Root", "A", "B", "AA", "AB", "BA", "BB"],
        parents=["", "root", "root", "A", "A", "B", "B"],
        branchvalues="total"
    ))

    fig.update_layout(margin=dict(t=0, l=0, r=0, b=0))
    return fig

def create_sunburst_chart(df):
    # Data transformation for sunburst chart
    df['id'] = df['Subgroup']
    df['parent'] = df['Group']
    df['label'] = df['Subgroup Description']

    # Adding root node
    root_df = pd.DataFrame({
        'id': ['root'],
        'parent': [None],
        'label': ['CPC Classifications']
    })
    df = pd.concat([root_df, df])

    # Print DataFrame structure (for debugging)
    print(df[['id', 'label', 'parent']].head())

    # Creating the sunburst chart
    fig = go.Figure(go.Sunburst(
        ids=df['id'],
        labels=df['label'],
        parents=df['parent'],
        branchvalues="total"
    ))

    fig.update_layout(margin=dict(t=0, l=0, r=0, b=0))
    return fig

# Testing with a simple example
test_chart = create_test_sunburst_chart()
st.plotly_chart(test_chart)
y_tunnus = st.session_state.get('y_tunnus')
yritys_nimi = st.session_state.get('yritys')
# Create and display the sunburst chart from data
if y_tunnus:
    cpc_data = fetch_company_cpc_data(y_tunnus)
    cpc_data = make_cpc(cpc_data)
    st.dataframe(cpc_data)

    sunburst_chart = create_sunburst_chart(cpc_data)
    if sunburst_chart:
        st.plotly_chart(sunburst_chart)
    else:
        st.error("There was an issue creating the sunburst chart.")


# Create and display the sunburst chart
if y_tunnus:
    cpc_data = fetch_company_cpc_data(y_tunnus)
    cpc_data = make_cpc(cpc_data)
    st.dataframe(cpc_data)

    # Create the sunburst chart
    sunburst_chart = create_sunburst_chart(cpc_data)
    if sunburst_chart:
        st.plotly_chart(sunburst_chart)
    else:
        st.error("There was an issue creating the sunburst chart.")
     





            

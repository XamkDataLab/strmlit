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

def prepare_network_data(df):
    # Creating unique identifiers for each level to serve as nodes
    df['Section_ID'] = df['Section']
    df['Class_ID'] = df['Section'] + '-' + df['Class']
    df['Subclass_ID'] = df['Section'] + '-' + df['Class'] + '-' + df['Subclass']
    df['Group_ID'] = df['Section'] + '-' + df['Class'] + '-' + df['Subclass'] + '-' + df['Group']
    df['Subgroup_ID'] = df['Section'] + '-' + df['Class'] + '-' + df['Subclass'] + '-' + df['Group'] + '-' + df['Subgroup']

    # Create nodes DataFrame
    nodes = pd.concat([
        df['Section_ID'].drop_duplicates(),
        df['Class_ID'].drop_duplicates(),
        df['Subclass_ID'].drop_duplicates(),
        df['Group_ID'].drop_duplicates(),
        df['Subgroup_ID'].drop_duplicates()
    ]).reset_index(drop=True).reset_index().rename(columns={0: 'Node', 'index': 'ID'})

    # Create edges DataFrame
    edges = pd.concat([
        df[['Section_ID', 'Class_ID']].drop_duplicates(),
        df[['Class_ID', 'Subclass_ID']].drop_duplicates(),
        df[['Subclass_ID', 'Group_ID']].drop_duplicates(),
        df[['Group_ID', 'Subgroup_ID']].drop_duplicates()
    ])

    # Map edges to node IDs
    edges = edges.applymap(lambda x: nodes[nodes['Node'] == x]['ID'].values[0])

    return nodes, edges

# Function to create the network graph
def create_network_graph(nodes, edges):
    fig = go.Figure()

    # Add edges
    for _, edge in edges.iterrows():
        fig.add_trace(go.Scatter(
            x=[nodes.loc[edge[0], 'ID'], nodes.loc[edge[1], 'ID']],
            y=[nodes.loc[edge[0], 'ID'], nodes.loc[edge[1], 'ID']],
            mode='lines',
            line=dict(width=1, color='grey'),
            hoverinfo='none'
        ))

    # Add nodes
    fig.add_trace(go.Scatter(
        x=nodes['ID'],
        y=nodes['ID'],
        mode='markers+text',
        text=nodes['Node'],
        textposition='bottom center',
        marker=dict(size=10, color='LightSkyBlue')
    ))

    fig.update_layout(plot_bgcolor='white', xaxis={'visible': False}, yaxis={'visible': False})

    return fig

y_tunnus = st.session_state.get('y_tunnus')
yritys_nimi = st.session_state.get('yritys')

if y_tunnus:
    cpc_data = fetch_company_cpc_data(y_tunnus)
    cpc_data = make_cpc(cpc_data)
    st.dataframe(cpc_data)
    nodes, edges = prepare_network_data(cpc_data)
    fig = create_network_graph(nodes, edges)
    st.plotly_chart(fig)
    



            

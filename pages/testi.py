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

    # Create nodes and edges
    nodes = pd.concat([
        df['Section_ID'].drop_duplicates(),
        df['Class_ID'].drop_duplicates(),
        df['Subclass_ID'].drop_duplicates(),
        df['Group_ID'].drop_duplicates(),
        df['Subgroup_ID'].drop_duplicates()
    ]).reset_index(drop=True)

    edges = pd.concat([
        df[['Section_ID', 'Class_ID']].drop_duplicates(),
        df[['Class_ID', 'Subclass_ID']].drop_duplicates(),
        df[['Subclass_ID', 'Group_ID']].drop_duplicates(),
        df[['Group_ID', 'Subgroup_ID']].drop_duplicates()
    ])

    return nodes, edges

# Function to create the network graph
def create_network_graph(nodes, edges):
    edge_x = []
    edge_y = []
    for edge in edges.values:
        x0, y0 = nodes.get_loc(edge[0]), nodes.get_loc(edge[1])
        edge_x.extend([x0, y0, None])
        edge_y.extend([y0, y0, None])

    node_x = list(range(len(nodes)))

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=node_x, y=node_x,
        mode='markers',
        text=nodes,
        marker=dict(size=10, color='LightSkyBlue')
    ))

    fig.add_trace(go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=1, color='grey'),
        hoverinfo='none',
        mode='lines'))

    fig.update_layout(plot_bgcolor='white')

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
    



            

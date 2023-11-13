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

   
y_tunnus = st.session_state.get('y_tunnus')
yritys_nimi = st.session_state.get('yritys')

if y_tunnus:
    cpc_data = fetch_company_cpc_data(y_tunnus)
    cpc_data = make_cpc(cpc_data)
    st.dataframe(cpc_data)
    nodes, edges = prepare_network_data(cpc_data)
    fig = create_network_graph(nodes, edges)
    st.plotly_chart(fig)
    

    dot = gv.Digraph(comment='CPC Classification', format='png')

    # Add nodes and edges based on the CPC classification hierarchy
    # The following is an example based on assuming unique identifiers per classification level
    for _, row in cpc_data.iterrows():
        # Add nodes
        dot.node(row['Section'])
        dot.node(row['Class'])
        dot.node(row['Subclass'])
        dot.node(row['Group'])
        dot.node(row['Subgroup'])
        
        # Add edges
        dot.edge(row['Section'], row['Class'])
        dot.edge(row['Class'], row['Subclass'])
        dot.edge(row['Subclass'], row['Group'])
        dot.edge(row['Group'], row['Subgroup'])
    
        # Render the graph to a file (this will save the file in the current directory)
        dot.render('cpc_classification_tree')
        
        # Display the graph using Streamlit
        st.graphviz_chart(dot)
        
     





            

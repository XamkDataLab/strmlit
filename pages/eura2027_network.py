import streamlit as st
import pandas as pd
import networkx as nx
import textwrap
import json  
from pyvis.network import Network
import streamlit.components.v1 as components
from queries import fetch_collaboration_data

data = fetch_eura2027_collab()

def create_graph(data):
    G = nx.Graph()
    for idx, row in data.iterrows():
        G.add_node(row['Organization1'], color='red', title=row['Organization1'])  
        G.add_node(row['Organization2'], color='blue', title=row['Organization2']) 
        G.add_edge(row['Organization1'], row['Organization2'], title=row['Group_Project_code'])
    return G

def filter_data(data, project_code=None, rahasto=None):
    filtered_data = data.copy()
    if project_code and project_code != 'None':
        filtered_data = filtered_data[filtered_data['Group_Project_code'] == project_code]
    if rahasto and rahasto != 'None':
        filtered_data = filtered_data[filtered_data['Rahasto'] == rahasto]
    return filtered_data

# Streamlit app updates
project_code = st.selectbox('Filter by Project Code', ['None'] + list(data['Group_Project_code'].unique()))
filtered_data = filter_data(data, project_code=project_code)

rahasto = st.selectbox('Filter by Rahasto', ['None'] + list(filtered_data['Rahasto'].unique()))
filtered_data = filter_data(filtered_data, project_code=project_code, rahasto=rahasto)

# Rest of the code remains the same


import streamlit as st
import pandas as pd
import networkx as nx
from pyvis.network import Network
import streamlit.components.v1 as components
from queries import fetch_eura2027_collab

data = fetch_eura2027_collab()
st.dataframe(data)

def create_graph(data):
    G = nx.Graph()
    for idx, row in data.iterrows():
        G.add_node(row['Organization1'], color='red', title=row['Organization1'])  
        G.add_node(row['Organization2'], color='blue', title=row['Organization2']) 
        G.add_edge(row['Organization1'], row['Organization2'], title=row['Group_Project_code'])
    return G

def filter_data(data, tukimuoto=None, tukitoimen_ala=None, rahoittava_viranomainen=None, sijainti=None, organization=None):
    filtered_data = data.copy()
    if tukimuoto and tukimuoto != 'None':
        filtered_data = filtered_data[filtered_data['Tukimuoto'] == tukimuoto]
    if tukitoimen_ala and tukitoimen_ala != 'None':
        filtered_data = filtered_data[filtered_data['Tukitoimen_ala'] == tukitoimen_ala]
    if rahoittava_viranomainen and rahoittava_viranomainen != 'None':
        filtered_data = filtered_data[filtered_data['Rahoittava_viranomainen'] == rahoittava_viranomainen]
    if sijainti and sijainti != 'None':
        filtered_data = filtered_data[filtered_data['Sijainti'] == sijainti]
    if organization:
        if 'None' in organization:
            organization.remove('None')
        if organization:
            filtered_data = filtered_data[(filtered_data['Organization1'].isin(organization)) | (filtered_data['Organization2'].isin(organization))]
    return filtered_data
    
def visualize_graph(graph):
    if graph.number_of_edges() > 0:
        nt = Network(notebook=False, height="500px", width="100%")
        
        for node, attr in graph.nodes(data=True):
            nt.add_node(node, color=attr.get('color', 'blue'), title=attr.get('title', ''))

        for u, v, attr in graph.edges(data=True):
            nt.add_edge(u, v, title=attr.get('title', ''))
        
        nt.save_graph("network.html")
        with open("network.html", "r", encoding="utf-8") as f:
            html = f.read()
        components.html(html, height=500)
    else:
        st.warning("No edges to display. Please select different filters.")

# Streamlit app
st.title('EURA2027 Collaboration Network')
st.text('Select filters to visualize the network graph.')

tukimuoto = st.selectbox('Filter by Tukimuoto', ['None'] + list(data['Tukimuoto'].unique()))
tukitoimen_ala = st.selectbox('Filter by Tukitoimen_ala', ['None'] + list(data['Tukitoimen_ala'].unique()))
rahoittava_viranomainen = st.selectbox('Filter by Rahoittava_viranomainen', ['None'] + list(data['Rahoittava_viranomainen'].unique()))
sijainti = st.selectbox('Filter by Sijainti', ['None'] + list(data['Sijainti'].unique()))
organization = st.multiselect('Filter by Organization', ['None'] + list(set(data['Organization1'].unique()) | set(data['Organization2'].unique())))

filtered_data = filter_data(data, tukimuoto=tukimuoto, tukitoimen_ala=tukitoimen_ala, rahoittava_viranomainen=rahoittava_viranomainen, sijainti=sijainti, organization=organization)

if tukimuoto != 'None' or tukitoimen_ala != 'None' or rahoittava_viranomainen != 'None' or sijainti != 'None' or organization:
    filtered_graph = create_graph(filtered_data)
    visualize_graph(filtered_graph)
else:
    st.warning('Choose at least one filter to create the graph')



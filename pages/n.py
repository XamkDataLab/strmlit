mport streamlit as st
import pandas as pd
import networkx as nx
import textwrap
import json  
from pyvis.network import Network
import streamlit.components.v1 as components
from queries import fetch_eura2027_collab

data = fetch_eura2027_collab()

def create_graph(data):
    G = nx.Graph()
    for idx, row in data.iterrows():
        G.add_node(row['Organization1'], color='red', title=row['Organization1'])  
        G.add_node(row['Organization2'], color='blue', title=row['Organization2']) 
        G.add_edge(row['Organization1'], row['Organization2'], title=row['Group_Project_code'])
    return G

def filter_data(data, tukimuoto=None, tukitoimen_ala=None, rahoittava_viranomainen=None, sijainti=None, organization=None):
    filtered_data = data.copy()
    # ... [Existing filters]
    if sijainti and sijainti != 'None':
        filtered_data = filtered_data[(filtered_data['Sijainti1'] == sijainti) | (filtered_data['Sijainti2'] == sijainti)]
    if organization and organization != 'None':
        filtered_data = filtered_data[(filtered_data['Organization1'] == organization) | (filtered_data['Organization2'] == organization)]
    return filtered_data
    
def visualize_graph(graph, gravitational_constant, central_gravity):
    if graph.number_of_edges() > 0:
        nt = Network(notebook=False, height="500px", width="100%")
        
        for node, attr in graph.nodes(data=True):
            nt.add_node(node, color=attr.get('color', 'blue'), title=attr.get('title', ''))

        for u, v, attr in graph.edges(data=True):
            nt.add_edge(u, v, title=attr.get('title', ''))
        
        physics_options = {
            "physics": {
                "barnesHut": {
                    "gravitationalConstant": gravitational_constant,
                    "centralGravity": central_gravity,
                    "springLength": 100,
                    "springConstant": 0.05,
                    "damping": 0.1,
                    "avoidOverlap": 0.1
                },
                "maxVelocity": 50,
                "minVelocity": 0.1,
                "solver": "barnesHut",
                "stabilization": {
                    "enabled": True,
                    "iterations": 1000,
                    "updateInterval": 25,
                    "onlyDynamicEdges": False,
                    "fit": True
                },
                "timestep": 0.3,
                "adaptiveTimestep": True
            }
        }
        nt.set_options(json.dumps(physics_options))  # Convert to JSON string
        
        nt.save_graph("network.html")
        with open("network.html", "r", encoding="utf-8") as f:
            html = f.read()
        components.html(html, height=500)
    else:
        st.warning("No edges to display. Please select different filters.")

# Streamlit app
st.title('EURA2027 collab network')
st.text('tekstiä tähän')


# New Filter UI elements for Sijainti and Organization
sijainti = st.selectbox('Filter by Sijainti', ['None'] + list(data['Sijainti1'].unique()) + list(data['Sijainti2'].unique()))
organization = st.selectbox('Filter by Organization', ['None'] + list(data['Organization1'].unique()) + list(data['Organization2'].unique()))
tukimuoto = st.selectbox('Filter by Tukimuoto', ['None'] + list(data['Tukimuoto'].unique()))
tukitoimen_ala = st.selectbox('Filter by Tukitoimen_ala', ['None'] + list(data['Tukitoimen_ala'].unique()))
rahoittava_viranomainen = st.selectbox('Filter by Rahoittava_viranomainen', ['None'] + list(data['Rahoittava_viranomainen'].unique()))

# Modify this line to include the new filters
filtered_data = filter_data(data, tukimuoto=tukimuoto, tukitoimen_ala=tukitoimen_ala, rahoittava_viranomainen=rahoittava_viranomainen, sijainti=sijainti, organization=organization)


gravitational_constant = st.slider('Gravitational Constant', min_value=-10000, max_value=0, value=-8000, step=100)
central_gravity = st.slider('Central Gravity', min_value=0.0, max_value=1.0, value=0.3, step=0.1)

if tukimuoto != 'None' or tukitoimen_ala != 'None' or rahoittava_viranomainen != 'None':
    filtered_graph = create_graph(filtered_data)
    visualize_graph(filtered_graph, gravitational_constant, central_gravity)
else:
    st.warning('Choose at least one filter to create the graph')

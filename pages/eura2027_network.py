import streamlit as st
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

def filter_data(data, project_code=None, rahasto=None):
    filtered_data = data.copy()
    if project_code and project_code != 'None':
        filtered_data = filtered_data[filtered_data['Group_Project_code'] == project_code]
    if rahasto and rahasto != 'None':
        filtered_data = filtered_data[filtered_data['Rahasto'] == rahasto]
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
st.title('Organizational Collaboration Network')
st.text('Visualizing collaborations based on project codes and funding sources') 

project_code = st.selectbox('Filter by Project Code', ['None'] + list(data['Group_Project_code'].unique()))
filtered_data = filter_data(data, project_code=project_code)

rahasto = st.selectbox('Filter by Rahasto', ['None'] + list(filtered_data['Rahasto'].unique()))
filtered_data = filter_data(filtered_data, project_code=project_code, rahasto=rahasto)

gravitational_constant = st.slider('Gravitational Constant', min_value=-10000, max_value=0, value=-8000, step=100)
central_gravity = st.slider('Central Gravity', min_value=0.0, max_value=1.0, value=0.3, step=0.1)

if project_code != 'None' or rahasto != 'None':
    filtered_graph = create_graph(filtered_data)
    visualize_graph(filtered_graph, gravitational_constant, central_gravity)
else:
    st.warning('Choose at least one filter to create the graph')


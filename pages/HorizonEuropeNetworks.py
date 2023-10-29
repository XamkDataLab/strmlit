import streamlit as st
import pandas as pd
import networkx as nx
from pyvis.network import Network
import streamlit.components.v1 as components
from queries import *

# Load the data
data = fetch_collaboration_data()

# Create a NetworkX graph
@st.cache
def create_graph():
    G = nx.Graph()
    for idx, row in data.iterrows():
        G.add_edge(row['FinnishOrgName'], row['CollaboratorOrgName'], title=row['euroSciVocTitle'], country=row['CollaboratorCountry'])
    return G

G = create_graph()

# Filter functions
def filter_graph_by_title(graph, title):
    filtered_edges = [(u, v) for u, v, d in graph.edges(data=True) if d['title'] == title]
    filtered_graph = graph.edge_subgraph(filtered_edges).copy()
    return filtered_graph

def filter_graph_by_country(graph, country):
    filtered_edges = [(u, v) for u, v, d in graph.edges(data=True) if d['country'] == country]
    filtered_graph = graph.edge_subgraph(filtered_edges).copy()
    return filtered_graph

# Visualization function
def visualize_graph(graph):
    nt = Network(notebook=False, height="500px", width="100%")
    nt.from_nx(graph)
    nt.save_graph("network.html")
    with open("network.html", "r", encoding="utf-8") as f:
        html = f.read()
    components.html(html, height=500)

# Streamlit app
st.title('Collaboration Network Visualization')

if st.checkbox('Filter by euroSciVocTitle'):
    titles = data['euroSciVocTitle'].unique()
    title = st.selectbox('Select Title', titles)
    filtered_graph = filter_graph_by_title(G, title)
    visualize_graph(filtered_graph)
else:
    st.warning('Select the checkbox to activate filtering by euroSciVocTitle')

if st.checkbox('Filter by CollaboratorCountry'):
    countries = data['CollaboratorCountry'].unique()
    country = st.selectbox('Select Country', countries)
    filtered_graph = filter_graph_by_country(G, country)
    visualize_graph(filtered_graph)
else:
    st.warning('Select the checkbox to activate filtering by CollaboratorCountry')

if st.checkbox('Show Full Network'):
    visualize_graph(G)
else:
    st.warning('Select the checkbox to show the full collaboration network')

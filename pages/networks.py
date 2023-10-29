import streamlit as st
import pandas as pd
import networkx as nx
from pyvis.network import Network
import streamlit.components.v1 as components
from queries import *

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
def filter_graph(graph, title=None, country=None, finnish_org=None):
    edges_to_keep = []
    for u, v, d in graph.edges(data=True):
        if (title is None or d['title'] == title) and (country is None or d['country'] == country) and (finnish_org is None or u == finnish_org):
            edges_to_keep.append((u, v))
    filtered_graph = graph.edge_subgraph(edges_to_keep).copy()
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

title = country = finnish_org = None

if st.checkbox('Filter by euroSciVocTitle'):
    titles = data['euroSciVocTitle'].unique()
    title = st.selectbox('Select Title', titles)
else:
    st.warning('Select the checkbox to activate filtering by euroSciVocTitle')

if st.checkbox('Filter by CollaboratorCountry'):
    countries = data['CollaboratorCountry'].unique()
    country = st.selectbox('Select Country', countries)
else:
    st.warning('Select the checkbox to activate filtering by CollaboratorCountry')

if st.checkbox('Filter by Finnish Organization'):
    finnish_orgs = data['FinnishOrgName'].unique()
    finnish_org = st.selectbox('Select Finnish Organization', finnish_orgs)
else:
    st.warning('Select the checkbox to activate filtering by Finnish Organization')

filtered_graph = filter_graph(G, title, country, finnish_org)
visualize_graph(filtered_graph)

import streamlit as st
import pandas as pd
import networkx as nx
from pyvis.network import Network
import streamlit.components.v1 as components
from queries import *

import streamlit as st

if st.button('Clear Cache'):
    st.caching.clear_cache()
    st.success('Cache cleared!')

data = fetch_collaboration_data()


# Create a NetworkX graph
def create_graph():
    G = nx.Graph()
    for idx, row in data.iterrows():
        G.add_edge(row['FinnishOrgName'], row['CollaboratorOrgName'], title=row['euroSciVocTitle'], country=row['CollaboratorCountry'])
    return G

G = create_graph()

def filter_graph(graph, title=None, country=None, finnish_org=None):
    edges_to_keep = []
    for u, v, d in graph.edges(data=True):
        if (title is None or title == 'None' or d['title'] == title) and (country is None or country == 'None' or d['country'] == country) and (finnish_org is None or finnish_org == 'None' or u == finnish_org):
            edges_to_keep.append((u, v))
    filtered_graph = graph.edge_subgraph(edges_to_keep).copy()
    return filtered_graph

def visualize_graph(graph):
    if graph.number_of_edges() > 0:
        nt = Network(notebook=False, height="500px", width="100%")
        nt.from_nx(graph)
        nt.save_graph("network.html")
        with open("network.html", "r", encoding="utf-8") as f:
            html = f.read()
        components.html(html, height=500)
    else:
        st.warning("No edges to display. Please select different filters.")

# Streamlit app
st.title('Collaboration Network Visualization')

finnish_orgs = ['None'] + list(data['FinnishOrgName'].unique())
finnish_org = st.selectbox('Filter by Finnish Organization', finnish_orgs)

if finnish_org != 'None':
    # Filter titles and countries based on selected organization
    titles = ['None'] + list(data[data['FinnishOrgName'] == finnish_org]['euroSciVocTitle'].unique())
    countries = ['None'] + list(data[data['FinnishOrgName'] == finnish_org]['CollaboratorCountry'].unique())
else:
    titles = ['None'] + list(data['euroSciVocTitle'].unique())
    countries = ['None'] + list(data['CollaboratorCountry'].unique())

title = st.selectbox('Filter by euroSciVocTitle', titles)
country = st.selectbox('Filter by CollaboratorCountry', countries)

if title != 'None' or country != 'None' or finnish_org != 'None':
    filtered_graph = filter_graph(G, title, country, finnish_org)
    visualize_graph(filtered_graph)
else:
    st.warning('Please select at least one filter to visualize the network.')
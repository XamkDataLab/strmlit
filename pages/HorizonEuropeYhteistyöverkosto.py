import streamlit as st
import pandas as pd
import networkx as nx
from pyvis.network import Network
import streamlit.components.v1 as components
from queries import *

data = fetch_collaboration_data()

# Create a NetworkX graph
def create_graph(data):
    G = nx.Graph()
    for idx, row in data.iterrows():
        G.add_node(row['FinnishOrgName'], color='red')  # Finnish organizations colored red
        G.add_node(row['CollaboratorOrgName'], color='blue')  # Other nodes colored blue
        G.add_edge(row['FinnishOrgName'], row['CollaboratorOrgName'], title=row['euroSciVocTitle'], country=row['CollaboratorCountry'])
    return G

G = create_graph(data)

def filter_data(data, title=None, country=None, finnish_org=None):
    filtered_data = data.copy()
    if title and title != 'None':
        filtered_data = filtered_data[filtered_data['euroSciVocTitle'] == title]
    if country and country != 'None':
        filtered_data = filtered_data[filtered_data['CollaboratorCountry'] == country]
    if finnish_org and finnish_org != 'None':
        filtered_data = filtered_data[filtered_data['FinnishOrgName'] == finnish_org]
    return filtered_data

def visualize_graph(graph):
    if graph.number_of_edges() > 0:
        nt = Network(notebook=False, height="500px", width="100%")
        
        # Add nodes with color
        for node, attr in graph.nodes(data=True):
            nt.add_node(node, color=attr.get('color', 'blue'))  # Default to blue if no color is set
        
        # Add edges
        for u, v, attr in graph.edges(data=True):
            nt.add_edge(u, v)
        
        nt.save_graph("network.html")
        with open("network.html", "r", encoding="utf-8") as f:
            html = f.read()
        components.html(html, height=500)
    else:
        st.warning("No edges to display. Please select different filters.")

# Streamlit app
st.title('Horizon Europe yhteistyöverkostokaavio')
st.text('Hankekonsortiot joissa mukana vähintään yksi suomalainen yritys. 
st.text('Konsortioiden yhteenlaskettu rahoitus')

title = st.selectbox('Suodata aiheen mukaan', ['None'] + list(data['euroSciVocTitle'].unique()))
filtered_data = filter_data(data, title=title)

finnish_org = st.selectbox('Suodata organisaation mukaan', ['None'] + list(filtered_data['FinnishOrgName'].unique()))
filtered_data = filter_data(filtered_data, title=title, finnish_org=finnish_org)

country = st.selectbox('Suodata maan mukaan', ['None'] + list(filtered_data['CollaboratorCountry'].unique()))
filtered_data = filter_data(filtered_data, title=title, finnish_org=finnish_org, country=country)

if title != 'None' or country != 'None' or finnish_org != 'None':
    filtered_graph = create_graph(filtered_data)
    visualize_graph(filtered_graph)
else:
    st.warning('Valitse vähintään yksi suodatin luodaksesi verkostokaavion.')

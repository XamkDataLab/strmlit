import streamlit as st
import pandas as pd
import networkx as nx
from pyvis.network import Network
import streamlit.components.v1 as components
from queries import *  # Make sure to have this module and function defined

data = fetch_collaboration_data()

# Create a NetworkX graph
def create_graph(data):
    G = nx.Graph()
    for idx, row in data.iterrows():
        G.add_node(row['FinnishOrgName'], color='red', title=f"ProjectId: {row['ProjectId']}\nProjectTitle: {row['ProjectTitle']}")
        G.add_node(row['CollaboratorOrgName'], color='blue')
        G.add_edge(row['FinnishOrgName'], row['CollaboratorOrgName'], title=row['euroSciVocTitle'], country=row['CollaboratorCountry'])
    return G

G = create_graph(data)

def filter_data(data, title=None, country=None, finnish_org=None):
    # Filter data based on criteria
    # ...

# Streamlit app
st.title('Horizon Europe yhteistyöverkostokaavio')
st.text('Hankekonsortiot joissa mukana vähintään yksi suomalainen yritys.') 

title = st.selectbox('Suodata aiheen mukaan', ['None'] + list(data['euroSciVocTitle'].unique()))
filtered_data = filter_data(data, title=title)

finnish_org = st.selectbox('Suodata organisaation mukaan', ['None'] + list(filtered_data['FinnishOrgName'].unique()))
filtered_data = filter_data(filtered_data, title=title, finnish_org=finnish_org)

country = st.selectbox('Suodata maan mukaan', ['None'] + list(filtered_data['CollaboratorCountry'].unique()))
filtered_data = filter_data(filtered_data, title=title, finnish_org=finnish_org, country=country)

def visualize_graph(graph):
    if graph.number_of_edges() > 0:
        network_options = {
            "interaction": {"hover": True},
            "nodes": {
                "borderWidth": 2,
                "size": 30,
                "color": {
                    "border": "#222222",
                    "background": "#666666"
                },
                "font": {"color": "#eeeeee"}
            },
            "edges": {
                "color": "lightgray"
            }
        }
        nt = Network(notebook=False, height="500px", width="100%", options=network_options)
        
        for node, attr in graph.nodes(data=True):
            nt.add_node(node, color=attr.get('color', 'blue'), title=attr.get('title', ''))
        for u, v, attr in graph.edges(data=True):
            nt.add_edge(u, v)
        
        nt.save_graph("network.html")
        with open("network.html", "r", encoding="utf-8") as f:
            html = f.read()
        components.html(html, height=500)
    else:
        st.warning("No edges to display. Please select different filters.")

if title != 'None' or country != 'None' or finnish_org != 'None':
    filtered_graph = create_graph(filtered_data)
    visualize_graph(filtered_graph)
else:
    st.warning('Valitse vähintään yksi suodatin luodaksesi verkostokaavion.')



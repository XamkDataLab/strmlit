import streamlit as st
import pandas as pd
import numpy as np
from queries import *
import networkx as nx
import matplotlib.pyplot as plt

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

def prepare_data(cpc_data):
    cpc_columns_of_interest = [
        'cpc_code', 'Section', 'Class', 'Subclass', 'Group', 'Subgroup',
        'Section Description', 'Class Description', 'Subclass Description',
        'Group Description', 'Subgroup Description'
    ]
    cpc_hierarchy_data = cpc_data[cpc_columns_of_interest]
    cpc_hierarchy_data = cpc_hierarchy_data.drop_duplicates()
    cpc_hierarchy_data['unique_id'] = cpc_hierarchy_data[['Section', 'Class', 'Subclass', 'Group', 'Subgroup']].agg('-'.join, axis=1)
    return cpc_hierarchy_data

# Create the graph
def create_graph(cpc_hierarchy_data):
    G = nx.DiGraph()

    def add_nodes_edges(row, graph):
        hierarchy_levels = ['Section', 'Class', 'Subclass', 'Group', 'Subgroup']
        descriptions = [
            'Section Description',
            'Class Description',
            'Subclass Description',
            'Group Description',
            'Subgroup Description'
        ]
        for i, level in enumerate(hierarchy_levels):
            node_id = '-'.join(row[hierarchy_levels[:i+1]])
            if not graph.has_node(node_id):
                graph.add_node(node_id, description=row[descriptions[i]])
            if i != 0:
                parent_id = '-'.join(row[hierarchy_levels[:i]])
                graph.add_edge(parent_id, node_id)

    cpc_hierarchy_data.apply(lambda row: add_nodes_edges(row, G), axis=1)
    return G

# Visualize the graph
def visualize_graph(G):
    try:
        from networkx.drawing.nx_agraph import graphviz_layout
        layout = graphviz_layout
    except ImportError:
        try:
            from networkx.drawing.nx_pydot import graphviz_layout
            layout = graphviz_layout
        except ImportError:
            layout = nx.spring_layout
            print("Graphviz not available, using spring layout as fallback. For better results, install pygraphviz or pydot.")

    pos = layout(G, prog='dot')
    plt.figure(figsize=(15, 10))
    nx.draw(G, pos, with_labels=True, arrows=True, node_size=3000, node_color='lightblue', font_size=10, font_weight='bold', edge_color='gray')
    plt.title('CPC Hierarchy Visualization')
    plt.show()



    
    
y_tunnus = st.session_state.get('y_tunnus')
yritys_nimi = st.session_state.get('yritys')


# Create and display the sunburst chart
if y_tunnus:
    cpc_data = fetch_company_cpc_data(y_tunnus)
    cpc_data = make_cpc(cpc_data)
    st.dataframe(cpc_data)
    cpc_hierarchy_data = prepare_data(cpc_data)
    G = create_graph(cpc_hierarchy_data)
    visualize_graph(G)

     





            

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from queries import *

def get_emblem_url_from_github(maakunta_name):
    base_url = "https://raw.githubusercontent.com/XamkDataLab/strmlit/main/vaakunat"
    return f"{base_url}/{maakunta_name}.svg"

df = fetch_aggregated_data()

maakunnan_nimi_list = df['Maakunnan_nimi'].unique().tolist()
maakunnan_nimi_list.insert(0, "All")  

selected_maakunnan_nimi = st.selectbox('Select Maakunnan_nimi:', maakunnan_nimi_list)
col1, col2 = st.columns([1, 6])  # Adjust the numbers for desired column widths

if selected_maakunnan_nimi == "All":
    # Funding sources for the Sankey diagram
    sources = ['Total_Funding', 'Total_EU_Horizon_Funding', 'Total_Business_Finland_Funding', 'Total_Tutkimusrahoitus']
    maakunta_values = df['Maakunnan_nimi'].unique().tolist()  # Make sure this is updated with your actual unique values
    
    # Create lists to store Sankey diagram data
    source_indices = []
    target_indices = []
    values = []

    # Populate the lists with data
    for idx, source in enumerate(sources):
        grouped = df.groupby('Maakunnan_nimi')[source].sum()
        for maakunta_idx, maakunta in enumerate(maakunta_values):
            source_indices.append(idx)
            target_indices.append(len(sources) + maakunta_idx)
            values.append(grouped[maakunta])

    # Create the Sankey diagram
    fig = go.Figure(go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=sources + maakunta_values
        ),
        link=dict(
            source=source_indices,
            target=target_indices,
            value=values
        )
    ))
    
    # Display the Sankey diagram in Streamlit
    st.plotly_chart(fig)

else:
    emblem_url = get_emblem_url_from_github(selected_maakunnan_nimi)
    col1.image(emblem_url, width=100)
    df = df[df['Maakunnan_nimi'] == selected_maakunnan_nimi]
    st.write(df)


import streamlit as st
import pandas as pd
from queries import *

def get_emblem_url_from_github(maakunta_name):
    base_url = "https://raw.githubusercontent.com/XamkDataLab/strmlit/main/vaakunat"
    return f"{base_url}/{maakunta_name}.svg"


df = fetch_aggregated_data()

maakunnan_nimi_list = df['Maakunnan_nimi'].unique().tolist()
maakunnan_nimi_list.insert(0, "All")  

selected_maakunnan_nimi = st.selectbox('Select Maakunnan_nimi:', maakunnan_nimi_list)
col1, col2 = st.beta_columns([1,6])  # Adjust the numbers for desired column widths
if selected_maakunnan_nimi != "All":
    emblem_url = get_emblem_url_from_github(selected_maakunnan_nimi)
    #st.image(emblem_url, caption=f"Emblem for {selected_maakunnan_nimi}", use_column_width=True)
    col1.image(emblem_url, caption=f"Emblem for {selected_maakunnan_nimi}", width=100)
    st.write(emblem_url)

    df = df[df['Maakunnan_nimi'] == selected_maakunnan_nimi]

# Display the filtered dataframe
st.write(df)
# Create columns




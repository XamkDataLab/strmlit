import streamlit as st
import pandas as pd
from queries import *

# Fetch the data
df = fetch_aggregated_data()

# Create a unique list of Maakunnan_nimi values for the dropdown
maakunnan_nimi_list = df['Maakunnan_nimi'].unique().tolist()
maakunnan_nimi_list.insert(0, "All")  # Add an "All" option to show all data

# Create a dropdown menu and get the selected value
selected_maakunnan_nimi = st.selectbox('Select Maakunnan_nimi:', maakunnan_nimi_list)

# Filter the dataframe based on the dropdown selection
if selected_maakunnan_nimi != "All":
    df = df[df['Maakunnan_nimi'] == selected_maakunnan_nimi]

# Display the filtered dataframe
st.write(df)


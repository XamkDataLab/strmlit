import streamlit as st
import pandas as pd
from queries import *

def get_emblem_url_from_github(maakunta_name):
    # Replace 'YourGitHubUsername' and 'YourRepoName' with your actual details
    base_url = "https://raw.githubusercontent.com/YourGitHubUsername/YourRepoName/main/maakunta_emblems"
    return f"{base_url}/{maakunta_name}.svg"

# Fetch the data
df = fetch_aggregated_data()

# Create a unique list of Maakunnan_nimi values for the dropdown
maakunnan_nimi_list = df['Maakunnan_nimi'].unique().tolist()
maakunnan_nimi_list.insert(0, "All")  # Add an "All" option to show all data

# Create a dropdown menu and get the selected value
selected_maakunnan_nimi = st.selectbox('Select Maakunnan_nimi:', maakunnan_nimi_list)

# If a specific maakunta is selected (not "All"), display its emblem
if selected_maakunnan_nimi != "All":
    emblem_url = get_emblem_url_from_github(selected_maakunnan_nimi)
    st.image(emblem_url, caption=f"Emblem for {selected_maakunnan_nimi}", use_column_width=True)

    # Filter the dataframe based on the dropdown selection
    df = df[df['Maakunnan_nimi'] == selected_maakunnan_nimi]

# Display the filtered dataframe
st.write(df)



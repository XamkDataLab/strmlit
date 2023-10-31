import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.graph_objects as go
from queries import *

def get_emblem_url_from_github(maakunta_name):
    base_url = "https://raw.githubusercontent.com/XamkDataLab/strmlit/main/vaakunat"
    return f"{base_url}/{maakunta_name}.svg"

def get_innovative_companies(data, maakunta):
    current_year = datetime.now().year
    innovative_companies = data[
        (data['Maakunnan_nimi'] == maakunta) &
        (data['yrityksen_rekisteröimispäivä'].dt.year > current_year - 3) &
        (data['Patent_Applications_Count'] > 0)
    ]
    return innovative_companies

def versatile_normalize_registration_date_v2(dataframe): 
    invalid_dates = []

    def convert_to_datetime(date_str):
        if pd.isnull(date_str):
            return date_str
        try:
            return pd.to_datetime(date_str, format='%Y-%m-%d')
        except ValueError:
            try:
                return pd.to_datetime(date_str, format='%d-%m-%Y')
            except ValueError:
                try:
                    return pd.to_datetime(date_str, format='%d.%m.%Y')
                except ValueError:
                    st.write(f"Failed to convert date string: {date_str}")
                    return date_str
    
    dataframe['yrityksen_rekisteröimispäivä'] = dataframe['yrityksen_rekisteröimispäivä'].apply(convert_to_datetime)
    return dataframe

df = fetch_aggregated_data()
df = versatile_normalize_registration_date_v2(df)
df = df[df['Maakunnan_nimi'].notna()]
# Define a dictionary with old column names as keys and new column names as values
column_rename_mapping = {
    'Total_Funding': 'EURA rahoitukset',
    'Total_Business_Finland_Funding': 'Business Finland avustukset',
    'Total_Tutkimusrahoitus': 'Business Finland tutkimusrahoitukset',
    'Total_EU_Horizon_Funding': 'Muut EU rahoitukset'
    # Add more columns as needed
}

df = df.rename(columns=column_rename_mapping)

maakunnan_nimi_list = df['Maakunnan_nimi'].unique().tolist()
maakunnan_nimi_list.insert(0, "All")  
selected_maakunnan_nimi = st.selectbox('Select Maakunnan_nimi:', maakunnan_nimi_list)

sources = ['EURA rahoitukset', 'Muut EU rahoitukset', 'Business Finland avustukset', 'Business Finland tutkimusrahoitukset']
selected_source = st.selectbox('Select Source:', ["All"] + sources)

if selected_maakunnan_nimi == "All":

    maakunta_values = df['Maakunnan_nimi'].unique().tolist()

    # Filter by the selected source if it's not "All"
    if selected_source != "All":
        sources = [selected_source]

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
    st.dataframe(df[['y_tunnus', 'yritys']])
    
    # ... [Same code for the "All" Sankey diagram]

else:
    emblem_url = get_emblem_url_from_github(selected_maakunnan_nimi)
    st.image(emblem_url, width=100)

    # Get the innovative companies for the selected Maakunta
    innovative_companies = get_innovative_companies(df, selected_maakunnan_nimi)

    # Display the title and the dataframe of innovative companies
    st.title('Uudet innovatiiviset yritykset')
    st.dataframe(innovative_companies[['y_tunnus', 'yritys', 'yrityksen_rekisteröimispäivä', 'Patent_Applications_Count']])
    st.dataframe(df[['y_tunnus', 'yritys', 'yrityksen_rekisteröimispäivä', 'Patent_Applications_Count']])

from collections import namedtuple
import altair as alt
import math
import streamlit as st
import numpy as np
import time
import plotly
import plotly.graph_objects as go

"""
# Aineettoman omaisuuden Suomi

Alueiden innovaatiotoiminnan kirjaamo

Xamk, Dadalabra, Luovat Alat

"""

# Load data (adjust paths as necessary)
patents_df = pd.read_csv('patents.csv')
patent_applicants_df = pd.read_csv('patent_applicants.csv')
merged_df = patents_df.merge(patent_applicants_df, on='lens_id', how='inner')

# Extract the year from the date_published column
merged_df['year_published'] = pd.to_datetime(merged_df['date_published']).dt.year

# Group the data by extracted_name, year_published, and jurisdiction
grouped_df = merged_df.groupby(['extracted_name', 'year_published', 'jurisdiction']).size().reset_index(name='frequency')

def create_heatmap(jurisdiction):
    filtered_data = grouped_df[grouped_df['jurisdiction'] == jurisdiction]

    fig = go.Figure(go.Heatmap(
        x=filtered_data['year_published'],
        y=filtered_data['extracted_name'],
        z=filtered_data['frequency'],
        colorscale='Viridis',
        colorbar=dict(title='Frequency')
    ))

    fig.update_layout(
        title=f"Patent Frequencies by Applicant and Year ({jurisdiction})",
        xaxis_title="Year Published",
        yaxis_title="Applicant Name"
    )

    return fig

# Streamlit app
st.title("Patent Frequencies Heatmap")
selected_jurisdiction = st.selectbox("Select Jurisdiction", grouped_df['jurisdiction'].unique())
st.plotly_chart(create_heatmap(selected_jurisdiction))

#progress_bar = st.sidebar.progress(0)
#status_text = st.sidebar.empty()
#last_rows = np.random.randn(1, 1)
#chart = st.line_chart(last_rows)

#for i in range(1, 101):
    #new_rows = last_rows[-1, :] + np.random.randn(5, 1).cumsum(axis=0)
    #status_text.text("%i%% Complete" % i)
    #chart.add_rows(new_rows)
    #progress_bar.progress(i)
    #last_rows = new_rows
    #time.sleep(0.05)

#progress_bar.empty()

#st.button("Re-run")

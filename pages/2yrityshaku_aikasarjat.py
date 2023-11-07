import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import datetime
from queries import *

y_tunnus = st.session_state.get('y_tunnus')
st.title(f"Otsikko yritykselle {y_tunnus}")

if y_tunnus:
    patents_data, trademarks_data = fetch_time_series_data(y_tunnus)

    # Display the patents data
    st.subheader("Patent Data")
    st.dataframe(patents_data)

    # Display the trademarks data
    st.subheader("Trademark Data")
    st.dataframe(trademarks_data)

    patents_df['date_published'] = pd.to_datetime(patents_df['date_published'])
    trademarks_df['applicationDate'] = pd.to_datetime(trademarks_df['applicationDate'])

    patents_df = patents_df.sort_values(by='date_published')
    trademarks_df = trademarks_df.sort_values(by='applicationDate')

    patents_dtypes = patents_df.dtypes
    trademarks_dtypes = trademarks_df.dtypes

    patents_count = patents_df['date_published'].dt.date.value_counts().sort_index()
    trademarks_count = trademarks_df['applicationDate'].dt.date.value_counts().sort_index()

# Create traces for the plot
    trace_patents = go.Scatter(
        x=patents_count.index,
        y=patents_count.values,
        mode='lines+markers',
        name='Patents'
    )

    trace_trademarks = go.Scatter(
        x=trademarks_count.index,
        y=trademarks_count.values,
        mode='lines+markers',
        name='Trademarks'
    )

    # Layout for the plot
    layout = go.Layout(
        title='Patents and Trademarks Over Time',
        xaxis=dict(title='Date'),
        yaxis=dict(title='Count'),
        hovermode='closest'
    )

    # Create the figure
    fig = go.Figure(data=[trace_patents, trace_trademarks], layout=layout)

    # Show the figure
    fig.show()
    


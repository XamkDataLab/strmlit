import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from queries import * 

st.session_state['y_tunnus'] = y_tunnus

st.title(f"Otsikko yritykselle {y_tunnus}")

if y_tunnus:
    patents_df, trademarks_df = fetch_time_series_data(y_tunnus)

    if not patents_df.empty:
        # Display the patents data
        st.subheader("Patent Data")
        st.dataframe(patents_df)

        # Process patents data
        patents_df['date_published'] = pd.to_datetime(patents_df['date_published'])
        patents_df = patents_df.sort_values(by='date_published')
        patents_count = patents_df['date_published'].dt.date.value_counts().sort_index()

        # Plot patents data
        trace_patents = go.Scatter(
            x=patents_count.index,
            y=patents_count.values,
            mode='lines+markers',
            name='Patents'
        )

    if not trademarks_df.empty:
        # Display the trademarks data
        st.subheader("Trademark Data")
        st.dataframe(trademarks_df)

        trademarks_df['applicationDate'] = pd.to_datetime(trademarks_df['applicationDate'])
        trademarks_df = trademarks_df.sort_values(by='applicationDate')
        trademarks_count = trademarks_df['applicationDate'].dt.date.value_counts().sort_index()

        trace_trademarks = go.Scatter(
            x=trademarks_count.index,
            y=trademarks_count.values,
            mode='lines+markers',
            name='Trademarks'
        )

    if not patents_df.empty and not trademarks_df.empty:
        layout = go.Layout(
            title='Patents and Trademarks Over Time',
            xaxis=dict(
                title='Date',
                dtick="M2",  # Ticks every two months
                tickformat="%b %Y"  # Formatting the tick labels to show abbreviated month and full year
            ),
            yaxis=dict(
                title='Count',
                range=[0, max(patents_count.max(), trademarks_count.max()) + 1]
            ),
            hovermode='closest'
        )

        fig = go.Figure(data=[trace_patents, trace_trademarks], layout=layout)

        st.plotly_chart(fig)
    elif patents_df.empty and trademarks_df.empty:
        st.write("No data available for the provided Y-Tunnus.")




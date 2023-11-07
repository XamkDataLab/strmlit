import streamlit as st
import pandas as pd
import plotly.express as px
from queries import * 

y_tunnus = st.session_state['y_tunnus]
st.title(f"Otsikko yritykselle {y_tunnus}")

if y_tunnus:
    patents_df, trademarks_df = fetch_time_series_data(y_tunnus)

    
    if not patents_df.empty:
        patents_df['year'] = patents_df['date_published'].dt.year
        patents_by_year = patents_df.groupby('year').size().reset_index(name='Patents')

    if not trademarks_df.empty:
        trademarks_df['year'] = trademarks_df['applicationDate'].dt.year
        trademarks_by_year = trademarks_df.groupby('year').size().reset_index(name='Trademarks')

    if not patents_df.empty and not trademarks_df.empty:
        combined_df = pd.merge(patents_by_year, trademarks_by_year, on='year', how='outer').fillna(0)

        fig = px.bar(
            combined_df,
            x='year',
            y=['Patents', 'Trademarks'],
            barmode='group',
            title='Number of Patents and Trademarks by Year'
        )

        st.plotly_chart(fig)
    else:
        st.write("No data available for the provided Y-Tunnus.")



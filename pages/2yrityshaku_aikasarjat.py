import streamlit as st
import pandas as pd
import plotly.express as px
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

    # You can also plot the data if they have a time component
    # Assuming the dates are in 'event_date' column for both patents and trademarks
    # and you want to plot the counts of patents and trademarks over time

    # Combine the dataframes for plotting
    combined_data = pd.concat([
        patents_data.assign(type='Patent'),
        trademarks_data.assign(type='Trademark')
    ])

    # Plotting
    if not combined_data.empty:
        # Convert event_date to datetime if not already
        combined_data['event_date'] = pd.to_datetime(combined_data['event_date'])
        combined_data = combined_data.sort_values('event_date')

        # Create a plot with Plotly Express
        fig = px.line(combined_data, x='event_date', color='type', markers=True,
                      title='Patents and Trademarks Over Time')

        # Display the plot
        st.plotly_chart(fig)
else:
    st.write("Invalid or missing parameters.")

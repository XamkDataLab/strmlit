from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st


"""
# Aineettoman omaisuuden Suomi

Alueiden innovaatiotoiminnan kirjaamo

Xamk, Dadalabra, Luovat Alat

"""




# Create a simple scatter plot using Plotly
fig = go.Figure(data=go.Scatter(x=[1, 2, 3, 4], y=[10, 11, 12, 13]))

# Set title
fig.update_layout(title='Simple Scatter Plot')

# Display the plot in Streamlit
st.plotly_chart(fig)


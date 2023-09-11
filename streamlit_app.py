from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
#import plotly.express as px

"""
# Aineettoman omaisuuden Suomi

Alueiden innovaatiotoiminnan kirjaamo

Xamk, Dadalabra, Luovat Alat

"""


def main():
    #st.title("plotlyplot")

    # Sample data
    df = {
        'x': [1, 2, 3, 4, 5],
        'y': [2, 3, 4, 5, 6]
    }

    # Create a scatter plot
    fig = px.scatter(df, x='x', y='y', title='Simple Scatter Plot')

    # Display the plot in Streamlit
    st.plotly_chart(fig)

if __name__ == "__main__":
    main()

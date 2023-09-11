from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
import plotly.express as px

"""
# Welcome to Streamlit!

Edit `/streamlit_app.py` to customize this app to your heart's desire :heart: ::P:

If you have any questions, checkout our [documentation](https://docs.streamlit.io) and [community
forums](https://discuss.streamlit.io).

In the meantime, below is an example of what you can do with just a few lines of code:
"""


def main():
    st.title("Simple Scatter Plot with Plotly and Streamlit")

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

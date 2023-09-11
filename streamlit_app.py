from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st

print("Hello World")
"""
# Aineettoman omaisuuden Suomi

Alueiden innovaatiotoiminnan kirjaamo


"""


import streamlit as st
import plotly.graph_objects as go

def main():
    st.title("Crude Representation of Finland with Adjustable Borders")

    # Function to bend the borders based on slider values
    def update_coords(top_bend, bottom_bend):
        return [0, 1+bottom_bend, 1+top_bend, 0, 0], [0, 0, 1, 1, 0]

    # Initial coordinates for the crude representation of Finland
    x = [0, 1, 1, 0, 0]
    y = [0, 0, 1, 1, 0]

    # Create the plot
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=x, y=y, fill='toself', mode='lines'))

    # Add sliders
    sliders = [
        # Slider for top bend
        {
            'active': 0,
            'yanchor': 'top',
            'xanchor': 'left',
            'currentvalue': {
                'font': {'size': 20},
                'prefix': 'Top Bend: ',
                'visible': True,
                'xanchor': 'right'
            },
            'transition': {'duration': 300, 'easing': 'cubic-in-out'},
            'pad': {'b': 10, 't': 50},
            'len': 0.9,
            'x': 0.1,
            'y': 0,
            'steps': [{
                'args': [[x, *update_coords(val*0.1, (1-val)*0.1)], {'frame': {'duration': 300, 'redraw': True}, 'mode': 'immediate'}],
                'label': str(val),
                'method': 'restyle'
            } for val in range(10)]
        },
        # Slider for bottom bend
        {
            'active': 0,
            'yanchor': 'top',
            'xanchor': 'left',
            'currentvalue': {
                'font': {'size': 20},
                'prefix': 'Bottom Bend: ',
                'visible': True,
                'xanchor': 'right'
            },
            'transition': {'duration': 300, 'easing': 'cubic-in-out'},
            'pad': {'b': 10, 't': 50},
            'len': 0.9,
            'x': 0.1,
            'y': 0.1,
            'steps': [{
                'args': [[x, *update_coords((1-val)*0.1, val*0.1)], {'frame': {'duration': 300, 'redraw': True}, 'mode': 'immediate'}],
                'label': str(val),
                'method': 'restyle'
            } for val in range(10)]
        }
    ]

    fig.update_layout(sliders=sliders)
    
    # Display the plot in Streamlit
    st.plotly_chart(fig)

if __name__ == "__main__":
    main()

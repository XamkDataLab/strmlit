import streamlit as st
import pandas as pd
import plotly.express as px
from queries import *

def generate_project_viz(df):
    # Convert the start and end date columns to datetime format
    df['Project start date'] = pd.to_datetime(df['Project start date'])
    df['Project end date'] = pd.to_datetime(df['Project end date'])

    # Create a custom column for the hover information
    df['Hover Info'] = 'Budget: ' + df['Beneficiary’s contracted amount (EUR)'].astype(str)

    # Create the Gantt chart using plotly
    fig = px.timeline(df, x_start="Project start date", x_end="Project end date", y="Subject of grant or contract", 
                      color="Subject of grant or contract", 
                      hover_name="Subject of grant or contract", 
                      hover_data=["Hover Info"], 
                      title="Projects Time Ranges and Budgets")

    fig.update_yaxes(categoryorder="total ascending")  # Sort projects based on start date
    fig.update_traces(marker_line_width=df['Beneficiary’s contracted amount (EUR)']/500000)  # Set line width based on budget
    
    fig.update_layout(showlegend=False)
    # Display the plot in Streamlit
    st.plotly_chart(fig)

# Retrieve the yritys_basename from session state
yritys_basename = st.session_state.get('yritys_basename2')
st.title(f"EU Horizon hankkeet yrityksessä {yritys_basename}")

# Fetch the data and generate the visualization
if yritys_basename:
    data = fetch_horizon_data(yritys_basename)
    if not data.empty:
        generate_project_viz(data)
    else:
        st.write("No data found.")
else:
    st.write("Invalid or missing parameters.")


#yritys_basename = st.session_state.get('yritys_basename2')
#st.title(f"EU Horizon rahoitus yritykselle {yritys_basename}")
#st.write(f"Debug: yritys_basename = {yritys_basename}")

#if yritys_basename:
 #   data = fetch_horizon_data(yritys_basename)
  #  if not data.empty:
   #     st.dataframe(data)
    #else:
     #   st.write("No data found.")
#else:
 #   st.write("Invalid or missing parameters.")



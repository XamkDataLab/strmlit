import streamlit as st
import pandas as pd
import plotly.express as px
import datetime
from queries import *

def truncate_text(text, max_length):
    return text if len(text) <= max_length else text[:max_length] + "..."

def generate_project_viz(df, filter_ended=True):
    # Convert the start and end date columns to datetime format
    df['Project start date'] = pd.to_datetime(df['Project start date'])
    df['Project end date'] = pd.to_datetime(df['Project end date'])

    # Filter only ongoing projects if required
    if filter_ended:
        today = pd.Timestamp(datetime.date.today())

        df = df[df['Project end date'] > today]

    # Add a truncated name column
    max_length = 60
    df['Truncated Name'] = df['Subject of grant or contract'].apply(lambda x: truncate_text(x, max_length))

    # Create a custom column for the hover information
    df['Hover Info'] = 'Budget: ' + df['Beneficiary’s contracted amount (EUR)'].astype(str)

    # Create the Gantt chart using plotly
    fig = px.timeline(df, x_start="Project start date", x_end="Project end date", y="Truncated Name", 
                      color="Truncated Name", 
                      hover_name="Subject of grant or contract", 
                      hover_data=["Hover Info"], 
                      title="Hankkeet")

    fig.update_yaxes(categoryorder="total ascending")  # Sort projects based on start date
    fig.update_traces(marker_line_width=df['Beneficiary’s contracted amount (EUR)']/500000)  # Set line width based on budget

    # Remove the color legend
    fig.update_layout(showlegend=False)
    
    # Hide the y-axis label
    fig.update_layout(yaxis_title_text="")

    # Display the plot in Streamlit
    st.plotly_chart(fig)


# Retrieve the yritys_basename from session state
yritys_basename = st.session_state.get('yritys_basename2')
st.title(f"EU muu rahoitus yritykselle {yritys_basename}")

if yritys_basename:
    data = fetch_horizon_data(yritys_basename)
else:
    st.write("Invalid or missing parameters.")
    data = pd.DataFrame()

programme_options = ["All"] + sorted(data["Programme name"].unique().tolist())
selected_programme = st.selectbox("Select Programme", programme_options)

# Filter Data based on selected programme
if selected_programme != "All":
    data = data[data["Programme name"] == selected_programme]

# Check if 'filter_ended' is in session state, if not initialize it
if 'filter_ended' not in st.session_state:
    st.session_state.filter_ended = False

if st.button("Piilota loppuneet projektit" if not st.session_state.filter_ended else "Näytä loppuneet projektit"):
    st.session_state.filter_ended = not st.session_state.filter_ended

# Generate the visualization
if not data.empty:
    generate_project_viz(data, st.session_state.filter_ended)
else:
    st.write("No data found.")

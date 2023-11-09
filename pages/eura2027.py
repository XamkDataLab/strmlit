import streamlit as st
import pandas as pd
import plotly.express as px
import datetime
from queries import *


def truncate_text(text, max_length):
    return text if len(text) <= max_length else text[:max_length] + "..."


def generate_eura_project_viz(df, filter_ended=True):
   
    df['Start_date'] = pd.to_datetime(df['Start_date'])
    df['End_date'] = pd.to_datetime(df['End_date'])

    # Filter only ongoing projects if required
    if filter_ended:
        today = pd.Timestamp(datetime.date.today())
        df = df[df['End_date'] > today]

    # Add a truncated name column
    max_length = 60
    df['Truncated Name'] = df['Project_name'].apply(lambda x: truncate_text(x, max_length))

    # Create a custom column for the hover information
    df['Hover Info'] = 'Budget: ' + df['Planned_public_funding'].astype(str)

    # Create the Gantt chart using plotly
    fig = px.timeline(df, x_start="Start_date", x_end="End_date", y="Truncated Name",
                      color="Truncated Name",
                      hover_name="Project_name",
                      hover_data=["Hover Info"],
                      title="EURA2027 Projects")

    fig.update_yaxes(categoryorder="total ascending")  # Sort projects based on start date
    # Set line width based on budget
    fig.update_traces(marker_line_width=df['Planned_public_funding']/500000)

    # Remove the color legend
    fig.update_layout(showlegend=False)

    # Hide the y-axis label
    fig.update_layout(yaxis_title_text="")

    # In a real Streamlit app, we would display the plot using st.plotly_chart(fig)
    st.plotly_chart(fig)


# Retrieve the yritys_basename from session state
y_tunnus = st.session_state.get('y_tunnus')
yritys_basename = st.session_state.get('yritys_basename2')
#st.write(st.session_state)
st.title(f"EURA2027 rahoitus yritykselle {yritys_basename}")

if y_tunnus:
    data = fetch_new_eura_data(y_tunnus)
    st.dataframe(data)
else:
    st.write("Invalid or missing parameters.")
    data = pd.DataFrame()

toimintalinja_options = ["All"] + sorted(data["Tukimuoto"].unique().tolist())
selected_toimintalinja = st.selectbox("Valitse tukimuoto", toimintalinja_options)

# Filter Data based on selected programme
if selected_toimintalinja != "All":
    data = data[data["Tukimuoto"] == selected_toimintalinja]

# Check if 'filter_ended' is in session state, if not initialize it
if 'filter_ended' not in st.session_state:
    st.session_state.filter_ended = False

if st.button("Piilota loppuneet projektit" if not st.session_state.filter_ended else "Näytä loppuneet projektit"):
    st.session_state.filter_ended = not st.session_state.filter_ended

# Generate the visualization
if not data.empty:
    generate_eura_project_viz(data, st.session_state.filter_ended)
else:
    st.write("No data found.")

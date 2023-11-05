import streamlit as st

# Function to get the URL of an emblem from GitHub
def get_emblem_url_from_github(maakunta_name):
    base_url = "https://raw.githubusercontent.com/XamkDataLab/strmlit/main/vaakunat"
    return f"{base_url}/{maakunta_name}.svg"

# Function to create a ribbon of emblems
def create_emblem_ribbon(maakunta_names):
    # Displaying emblems in a horizontal layout using columns
    cols = st.columns(len(maakunta_names))
    for col, maakunta_name in zip(cols, maakunta_names):
        with col:
            emblem_url = get_emblem_url_from_github(maakunta_name)
            st.image(emblem_url, use_column_width='auto', caption=maakunta_name)

# List of maakunta names (example names provided, replace with actual names)
maakunta_names = ["uusimaa", "pirkanmaa", "varsinais-suomi"]

# Title and introduction
st.title("Welcome to the Regional Emblem App")
st.write("This application showcases the emblems of various Finnish regions, "
         "providing a glimpse into the local heritage and symbols.")

# Emblem ribbon
st.header("Regional Emblems")
create_emblem_ribbon(maakunta_names)

# About the App
st.subheader("About the App")
st.write(
    """
    Explore the rich cultural tapestry of Finland through our collection of regional emblems. 
    Each emblem has its own story and significance, reflecting the identity and history of its region. 
    Navigate through the app to learn more about these fascinating symbols.
    """
)


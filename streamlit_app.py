import streamlit as st
import urllib.parse

# Function to get the URL of an emblem from GitHub, encoding the filename to handle special characters
def get_emblem_url_from_github(maakunta_name):
    base_url = "https://raw.githubusercontent.com/XamkDataLab/strmlit/main/vaakunat"
    # Ensure the filename is properly encoded to handle special characters like ä or ö
    encoded_maakunta_name = urllib.parse.quote(maakunta_name)
    return f"{base_url}/{encoded_maakunta_name}.svg"

# List of actual maakunta names
maakunta_names = [
    "Ahvenanmaa",
    "Etelä-Karjala",
    "Etelä-Pohjanmaa",
    "Etelä-Savo",
    "Kainuu",
    "Kanta-Häme",
    "Keski-Pohjanmaa",
    "Keski-Suomi",
    "Kymenlaakso",
    "Lappi",
    "Pirkanmaa",
    "Pohjanmaa",
    "Pohjois-Karjala",
    "Pohjois-Pohjanmaa",
    "Pohjois-Savo",
    "Päijät-Häme",
    "Satakunta",
    "Uusimaa",
    "Varsinais-Suomi"
]

# Display the emblem ribbon
# Adjust the number of columns based on the number of emblems to display per row
cols = st.columns(len(maakunta_names))
for idx, maakunta_name in enumerate(maakunta_names):
    with cols[idx]:
        emblem_url = get_emblem_url_from_github(maakunta_name)
        # Set a fixed width for the images to make them smaller
        st.image(emblem_url, width=50)  # Adjust the width as needed

# Main title and introduction
st.title("Welcome to the Regional Emblem App")

st.subheader("About the App")
st.write(
    """
    Explore the rich cultural tapestry of Finland through our collection of regional emblems. 
    Each emblem has its own story and significance, reflecting the identity and history of its region. 
    Navigate through the app to learn more about these fascinating symbols.
    """
)

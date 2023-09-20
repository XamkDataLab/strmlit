import pandas as pd
import pyodbc
import streamlit as st
from queries import * 

driver = st.secrets["driver"]
server = st.secrets["server"]
database = st.secrets["database"]
username = st.secrets["username"]
password = st.secrets["password"]

# Define custom styles
small_font_style = """
<style>
    .small-font {
        font-size: 16px;
    }
</style>
"""
medium_font_style = """
<style>
    .medium-font {
        font-size: 24px;
        font-weight: bold;
    }
</style>
"""

large_font_style = """
<style>
    .large-font {
        font-size: 38px;
    }
</style>
"""

large_number_style = """
<style>
    .large-number {
        font-size: 32px;   
    }
</style>
"""

st.markdown(small_font_style, unsafe_allow_html=True)
st.markdown(medium_font_style, unsafe_allow_html=True)
st.markdown(large_font_style, unsafe_allow_html=True)
st.markdown(large_number_style, unsafe_allow_html=True)

st.title('Hae yrityksen tiedot')
y_tunnus = st.text_input("Anna Y-tunnus (ja paina enter)")

if y_tunnus:
    data = fetch_data(y_tunnus)
    #st.write("Debug: Fetched data:")
    #st.write(data)

    if not data.empty:
        st.title(f"{data['yritys_basename'].iloc[0]} {data['y_tunnus'].iloc[0]}")
        st.markdown(f"<div class='large-font'>{data['yritys'].iloc[0]}</div>", unsafe_allow_html=True)

        card_content = f"""
        <div style="background-color: #f5f5f5; padding: 15px; border-radius: 5px;">
        <div class="medium-font">EURA-rahoitus päätoteuttajana</div>
        <div class="large-number">{data['Total_Funding'].iloc[0]} €</div>
        <div class="small-font">linkki tarkempiin tietoihin (esim. isoimmat hankkeet)</div>
        <hr>
        <div class="medium-font">Patenttien määrä</div>
        <div class="large-number">{data['Patent_Applications_Count'].iloc[0]}</div>
        <div class="small-font">linkki tarkempiin tietoihin (patenttilistaus + visualisoinnit)</div>
        <hr>
        <div class="medium-font">Tavaramerkkien määrä</div>
        <div class="large-number">{data['Trademarks_Count'].iloc[0]}</div>
         <div class="small-font">linkki tarkempiin tietoihin (sanat & kuvat?)</div>
        <hr>
        <div class="medium-font">Mallioikeuksien määrä</div>
        <div class="large-number">{data['Design_Rights_Count'].iloc[0]}</div>
         <div class="small-font">linkki tarkempiin tietoihin</div>
        </div>
        """
        st.markdown(card_content, unsafe_allow_html=True)

    else:
       st.write("Dataa ei löytynyt :(")



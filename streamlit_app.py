import streamlit as st
from queries import *

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

# Input for Y_tunnus
y_tunnus = st.text_input("Anna Y-tunnus (ja paina enter)")
st.session_state['y_tunnus'] = y_tunnus

# Function to format currency with space as thousands separator and add € symbol
def format_currency(number):
    return f"{number:,.0f} €".replace(",", " ")

# If a Y_tunnus is given, fetch and display the data
if y_tunnus:
    data = fetch_data(y_tunnus)

    if not data.empty:
        st.markdown(f"<div class='large-font'>{data['yritys'].iloc[0]}</div>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)  # Create two columns
    
        # Content for the first column
        card_content1 = f"""
        <div style="background-color: #f5f5f5; padding: 15px; border-radius: 5px;">
        <div class="medium-font">EU Horizon rahoitus 2013-2030</div>
        <div class="large-number">{format_currency(int(data['Total_EU_Horizon_Funding'].iloc[0]))}</div>
        <hr>
        <div class="medium-font">EURA-rahoitus 2014-2020 ohjelmakausi</div>
        <div class="large-number">{format_currency(int(data['Total_Funding'].iloc[0]))}</div>
        <div class="small-font">2021-2027 ohjelmakauden tietolähde julkaistaan lokakuun alussa</div>
        <hr>
        <div class="medium-font">Business Finland tuet</div>
        <div class="large-number">{format_currency(int(data['Total_Business_Finland_Funding'].iloc[0]))}</div>
        </div>
        """
        col1.markdown(card_content1, unsafe_allow_html=True)

        # Content for the second column
        card_content2 = f"""
        <div style="background-color: #f5f5f5; padding: 15px; border-radius: 5px;">
        <div class="medium-font">Patenttien määrä</div>
        <div class="large-number">{int(data['Patent_Applications_Count'].iloc[0]):,}</div>
        <hr>
        <div class="medium-font">Tavaramerkkien määrä</div>
        <div class="large-number">{int(data['Trademarks_Count'].iloc[0]):,}</div>
        <hr>
        <div class="medium-font">Mallioikeuksien määrä</div>
        <div class="large-number">{int(data['Design_Rights_Count'].iloc[0]):,}</div>
        </div>
        """
        col2.markdown(card_content2, unsafe_allow_html=True)

    else:
        st.write("Dataa ei löytynyt :(")

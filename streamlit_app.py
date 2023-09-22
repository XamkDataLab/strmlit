import streamlit as st
from queries import * 

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

# Input for Y_tunnus
y_tunnus = st.text_input("Anna Y-tunnus (ja paina enter)")
st.session_state['y_tunnus'] = y_tunnus
# If a Y_tunnus is given, fetch and display the data
if y_tunnus:
    data = fetch_data(y_tunnus)

    if not data.empty:
        st.markdown(f"<div class='large-font'>{data['yritys'].iloc[0]}</div>", unsafe_allow_html=True)
        
        # Card 1
        with st.container():
            st.markdown("<div class='medium-font'>EU Horizon rahoitus 2013-2030</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='large-number'>{int(data['Total_EU_Horizon_Funding'].iloc[0]):,}</div>", unsafe_allow_html=True)
            
            cols1 = st.columns(3)
            cols1[0].markdown("<div class='small-font'>EURA-rahoitus 2014-2020 ohjelmakausi</div>", unsafe_allow_html=True)
            cols1[1].markdown(f"<div class='large-number'>{int(data['Total_Funding'].iloc[0]):,} €</div>", unsafe_allow_html=True)
            cols1[2].markdown("<div class='small-font'><a href='/detailed_info?y_tunnus={y_tunnus}&type=Total_Funding'>linkki tarkempiin tietoihin</a></div>", unsafe_allow_html=True)

        st.write("")  # Add space between the cards
        
        # Card 2
        with st.container():
            st.markdown("<div class='medium-font'>Patenttien määrä</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='large-number'>{int(data['Patent_Applications_Count'].iloc[0]):,}</div>", unsafe_allow_html=True)
            
            cols2 = st.columns(3)
            cols2[0].markdown("<div class='small-font'>Tavaramerkkien määrä</div>", unsafe_allow_html=True)
            cols2[1].markdown(f"<div class='large-number'>{int(data['Trademarks_Count'].iloc[0]):,}</div>", unsafe_allow_html=True)
            cols2[2].markdown("<div class='small-font'><a href='/detailed_info?y_tunnus={y_tunnus}&type=Trademarks_Count'>linkki tarkempiin tietoihin</a></div>", unsafe_allow_html=True)

    else:
        st.write("Dataa ei löytynyt :(")


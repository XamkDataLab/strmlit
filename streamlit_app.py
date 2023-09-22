
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

# Function to format numbers with space as thousands separator and add € symbol
def format_currency(number):
    return f"{number:,.0f} €".replace(",", " ")

# If a Y_tunnus is given, fetch and display the data
if y_tunnus:
    st.session_state['y_tunnus'] = y_tunnus
    data = fetch_data(y_tunnus)

    if not data.empty:
        st.markdown(f"<div class='large-font'>{data['yritys'].iloc[0]}</div>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)

        # Content for the first column
        col1.write("EU Horizon rahoitus 2013-2030")
        col1.write(format_currency(int(data['Total_EU_Horizon_Funding'].iloc[0])))
        if col1.button("linkki tarkempiin tietoihin (hankkeet ja ohjelmat) - EU Horizon"):
            st.session_state.page = "Total_EU_Horizon_Funding"

        col1.write("EURA-rahoitus 2014-2020 ohjelmakausi")
        col1.write(format_currency(int(data['Total_Funding'].iloc[0])))
        if col1.button("linkki tarkempiin tietoihin (esim. isoimmat hankkeet) - EURA-rahoitus"):
            st.session_state.page = "Total_Funding"

        col1.write("Business Finland tuet")
        col1.write(format_currency(int(data['Total_Business_Finland_Funding'].iloc[0])))
        if col1.button("linkki tarkempiin tietoihin - Business Finland"):
            st.session_state.page = "Total_Business_Finland_Funding"

        # Content for the second column
        col2.write("Patenttien määrä")
        col2.write(data['Patent_Applications_Count'].iloc[0])
        if col2.button("linkki tarkempiin tietoihin (patenttilistaus + visualisoinnit)"):
            st.session_state.page = "Patent_Applications_Count"

        col2.write("Tavaramerkkien määrä")
        col2.write(data['Trademarks_Count'].iloc[0])
        if col2.button("linkki tarkempiin tietoihin (sanat & kuvat?) - Tavaramerkit"):
            st.session_state.page = "Trademarks_Count"

        col2.write("Mallioikeuksien määrä")
        col2.write(data['Design_Rights_Count'].iloc[0])
        if col2.button("linkki tarkempiin tietoihin - Mallioikeudet"):
            st.session_state.page = "Design_Rights_Count"

    else:
        st.write("Dataa ei löytynyt :(")

# Check the session state to display the correct page
if 'page' in st.session_state:
    y_tunnus_from_state = st.session_state.y_tunnus

    if st.session_state.page == "detailed_info":
        # Display the detailed info for Total EU Horizon Funding
        st.write(f"Details for EU Horizon with Y-tunnus: {y_tunnus_from_state}")
        # Fetch and display the relevant details using y_tunnus_from_state if needed

    elif st.session_state.page == "Total_Funding":
        st.write(f"Details for EURA-rahoitus with Y-tunnus: {y_tunnus_from_state}")
        # Fetch and display the relevant details using y_tunnus_from_state if needed

    elif st.session_state.page == "Total_Business_Finland_Funding":
        st.write(f"Details for Business Finland with Y-tunnus: {y_tunnus_from_state}")
        # Fetch and display the relevant details using y_tunnus_from_state if needed

    elif st.session_state.page == "Patent_Applications_Count":
        st.write(f"Details for Patenttien määrä with Y-tunnus: {y_tunnus_from_state}")
        # Fetch and display the relevant details using y_tunnus_from_state if needed

    elif st.session_state.page == "Trademarks_Count":
        st.write(f"Details for Tavaramerkkien määrä with Y-tunnus: {y_tunnus_from_state}")
        # Fetch and display the relevant details using y_tunnus_from_state if needed

    elif st.session_state.page == "Design_Rights_Count":
        st.write(f"Details for Mallioikeuksien määrä with Y-tunnus: {y_tunnus_from_state}")
        # Fetch and display the relevant details using y_tunnus_from_state if needed


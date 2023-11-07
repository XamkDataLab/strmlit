import streamlit as st
from queries import *
import pandas as pd
import plotly.express as px

small_font_style = """
<style>
    .small-font {
        font-size: 8px;
    }
</style>
"""
medium_font_style = """
<style>
    .medium-font {
        font-size: 12px;
        font-weight: bold;
    }
</style>
"""

large_font_style = """
<style>
    .large-font {
        font-size: 19px;
    }
</style>
"""

large_number_style = """
<style>
    .large-number {
        font-size: 16px;   
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
    data = fetch_data2(y_tunnus)
    #data2 = fetch_individual_data(y_tunnus)
    
    if not data.empty:
        st.markdown(f"<div class='large-font'>{data['yritys'].iloc[0]}</div>", unsafe_allow_html=True)
        
        yritys_basename = data['yritys_basename2'].iloc[0]
        st.session_state['yritys_basename2'] = yritys_basename
        #st.write(st.session_state)

        col1, col2, col3 = st.columns(3)  # Create two columns
    
        # Content for the first column
        card_content1 = f"""
        <div style="background-color: #f5f5f5; padding: 15px; border-radius: 5px;">
        <div class="medium-font">EU Horizon rahoitus 2013-2030</div>
        <div class="large-number">{format_currency(int(data['Total_EU_Horizon_Funding'].iloc[0]))}</div>
        <hr>
        <div class="medium-font">EURA-rahoitus 2014-2020 ohjelmakausi</div>
        <div class="large-number">{format_currency(int(data['Total_Funding'].iloc[0]))}</div>
        <div class="small-font">2021-2027 ohjelmakauden tietolähde julkaistaan lokakuun alussa</div>
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
        </div>
        """
        col2.markdown(card_content2, unsafe_allow_html=True)
        

        card_content3 = f"""
        <div style="background-color: #f5f5f5; padding: 15px; border-radius: 5px;">
        <div class="medium-font">Business Finland avustukset</div>
        <div class="large-number">{format_currency(int(data['Total_Business_Finland_Funding'].iloc[0]))}</div>
        <hr>
        <div class="medium-font">Business Finland tutkimusrahoitus</div>
        <div class="large-number">{int(data['Total_Tutkimusrahoitus'].iloc[0]):,}</div>
        </div>
        """
        col3.markdown(card_content3, unsafe_allow_html=True)
    
    else:
        st.write("Dataa ei löytynyt :(")

    if y_tunnus:
        patents_df, trademarks_df = fetch_time_series_data(y_tunnus)
        
        # Create a 'year' column for both patents and trademarks even if they might be empty
        patents_df['year'] = patents_df['date_published'].dt.year if not patents_df.empty else pd.Series(dtype=int)
        trademarks_df['year'] = trademarks_df['applicationDate'].dt.year if not trademarks_df.empty else pd.Series(dtype=int)
    
        # Group by year and count if not empty
        patents_by_year = patents_df.groupby('year').size().reset_index(name='Patents') if not patents_df.empty else pd.DataFrame({'year':[], 'Patents':[]})
        trademarks_by_year = trademarks_df.groupby('year').size().reset_index(name='Trademarks') if not trademarks_df.empty else pd.DataFrame({'year':[], 'Trademarks':[]})
    
        # Proceed with merging. The 'year' column will exist even if there are no records.
        combined_df = pd.merge(patents_by_year, trademarks_by_year, on='year', how='outer').fillna(0)
    
        # If the combined_df is not empty after the merge (i.e., at least one DataFrame had data)
        if not combined_df.empty:
            fig = px.bar(
                combined_df,
                x='year',
                y=['Patents', 'Trademarks'],
                barmode='group',
                title='Number of Patents and Trademarks by Year'
            )
    
            st.plotly_chart(fig)
        else:
            st.write("No data available for the provided Y-Tunnus.")


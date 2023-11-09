import streamlit as st
from queries import *
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go

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
    
def plot_time_series(df, title, date_col, money_cols):
    # Convert date column to just the year part
    df['year'] = df[date_col].dt.year

    # Group by year and sum the money columns
    df_grouped = df.groupby('year')[money_cols].sum().reset_index()

    fig = go.Figure()

    for money_col in money_cols:
        fig.add_trace(go.Scatter(x=df_grouped['year'], y=df_grouped[money_col], mode='lines', name=money_col))

    fig.update_layout(title=title, xaxis_title='Year', yaxis_title='Money', hovermode='closest')

    return fig


if y_tunnus:
    data = fetch_data2(y_tunnus)
    #data2 = fetch_individual_data(y_tunnus)
    #st.dataframe(data)
    if not data.empty:
        st.markdown(f"<div class='large-font'>{data['yritys'].iloc[0]}</div>", unsafe_allow_html=True)
        
        yritys_basename = data['yritys_basename2'].iloc[0]
        st.session_state['yritys_basename2'] = yritys_basename
        #st.write(st.session_state)

        col1, col2, col3 = st.columns(3)  # Create two columns
    
        # Content for the first column
        card_content1 = f"""
        <div style="background-color: #f5f5f5; padding: 15px; border-radius: 5px;">
        <div class="medium-font">EU rahoitus 2013-2030</div>
        <div class="large-number">{format_currency(int(data['Total_EU_Horizon_Funding'].iloc[0]))}</div>
        <hr>
        <div class="medium-font">EURA-rahoitus 2014-2020 ohjelmakausi</div>
        <div class="large-number">{format_currency(int(data['Total_Funding'].iloc[0]))}</div>
        <hr>
        <div class="medium-font">EURA-rahoitus 2021-2027 ohjelmakausi</div>
        <div class="large-number">{format_currency(int(data['Total_EURA2027_planned_funding'].iloc[0]))}</div>
        </div>
        """
        col1.markdown(card_content1, unsafe_allow_html=True)

        # Content for the second column
        card_content2 = f"""
        <div style="background-color: #f5f5f5; padding: 15px; border-radius: 5px;">
        <div class="medium-font">Patenttidokumenttien määrä</div>
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

    # Ensure 'year' columns are present even if dataframes are empty
    patents_df['year'] = patents_df['date_published'].dt.year if not patents_df.empty else pd.Series(dtype=int)
    trademarks_df['year'] = trademarks_df['applicationDate'].dt.year if not trademarks_df.empty else pd.Series(dtype=int)
    
    # Group by year and count if not empty
    patents_by_year = patents_df.groupby('year').size().reset_index(name='Patents') if not patents_df.empty else pd.DataFrame({'year':[], 'Patents':[]})
    trademarks_by_year = trademarks_df.groupby('year').size().reset_index(name='Trademarks') if not trademarks_df.empty else pd.DataFrame({'year':[], 'Trademarks':[]})
    
    # Merge and fill missing years
    combined_years = set(patents_by_year['year']).union(set(trademarks_by_year['year']))
    combined_df = pd.DataFrame({'year': list(combined_years)}).merge(patents_by_year, on='year', how='outer').merge(trademarks_by_year, on='year', how='outer').fillna(0)

    if not combined_df.empty:
        fig = px.bar(
            combined_df,
            x='year',
            y=['Patents', 'Trademarks'],
            barmode='group',
            title='Patenttidokumenttien ja tavaramerkkien määrä'
        )
        st.plotly_chart(fig)
    else:
        st.write("No data available for the provided Y-Tunnus.")

        
    if y_tunnus:
        EURA_df, BF_df, EURA2_df,EUmuu_df = fetch_time_series_data_funding(y_tunnus)
        #st.dataframe(EURA_df)
        #st.dataframe(BF_df)
        #st.dataframe(EURA2_df)
        #st.dataframe(EUmuu_df)
         
        BF_df['Myöntämisvuosi'] = pd.to_datetime(BF_df['Myöntämisvuosi'], format='%Y', errors='coerce')
        EURA2_df['Start_date'] = pd.to_datetime(EURA2_df['Start_date'], errors='coerce')
        EUmuu_df['Year'] = pd.to_datetime(EUmuu_df['Year'], format='%Y', errors='coerce')
        EURA_df['Aloituspvm'] = pd.to_datetime(EURA_df['Aloituspvm'], errors='coerce')
        
        dataframes = {
        'EURA2027': EURA_df,     # Assuming this has a single money column
        'Business Finland': BF_df,         # This has 'Myöntämisvuosi' and both 'Tutkimusrahoitus' & 'Avustus'
        'EURA2027': EURA2_df,   # This has 'Start_date' and 'Planned_EU_and_state_funding'
        'EU other': EUmuu_df    # This has 'Year' and 'Commitment contracted amount (EUR)'
        }

        # Dropdown to select the dataframe
        selected_df_name = st.selectbox('Select the dataframe:', list(dataframes.keys()))
    
        # Preprocessing the selected dataframe
        df = dataframes[selected_df_name].copy()
    
        # Setting up the date columns and money columns based on the selected dataframe
        date_col = None
        money_cols = []
        if selected_df_name == 'Business Finland':
            date_col = 'Myöntämisvuosi'
            money_cols = ['Tutkimusrahoitus', 'Avustus']
        elif selected_df_name == 'EURA2027':
            date_col = 'Start_date'
            money_cols = ['Planned_EU_and_state_funding']
        elif selected_df_name == 'EU other':
            date_col = 'Year'
            money_cols = ['Beneficiary’s contracted amount (EUR)']
        elif selected_df_name == 'EURA2020':
            date_col = 'Aloituspvm'
            money_cols = ['Toteutunut_EU_ja_valtion_rahoitus']
    
        # Plotting the time series data
        if date_col and money_cols:
            fig = plot_time_series(df, f'Time-Series for {selected_df_name}', date_col, money_cols)
            st.plotly_chart(fig)
        else:
            st.error("Error: Date or money columns not set correctly.")

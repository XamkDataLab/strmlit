import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from queries import *

# Define a function to transform the text
def transform_text(text):
    if pd.isna(text):  
        return None
    return ' '.join([word.capitalize() for word in text.split()])


render_mpl_table(filtered_df[['publication_type', 'Keksintö', 'Hakija', 'legal_status_anticipated_term_date', 'Link']], header_columns=0, col_width=2.0)



df = fetch_legal_status_data()
df['legal_status_anticipated_term_date'] = pd.to_datetime(df['legal_status_anticipated_term_date'])
df = df[df['legal_status_anticipated_term_date'].notna()]

current_date = datetime.today().strftime('%Y-%m-%d')
st.title(f"Yritysten erääntyviä patentteja {current_date}")

# Compute the 'Hakija' column
df['Hakija'] = df['yritys'].where(df['yritys'].notna(), df['extracted_name'].apply(transform_text))

option = st.selectbox('Näytä patentit jotka eräänyvät', ['3 kuukauden kuluessa', '6 kuukauden kuluessa', '12 kuukauden kuluessa'])

# Set the date range
min_date = datetime.today()
if option == '3 kuukauden kuluessa':
    max_date = min_date + timedelta(days=90)
elif option == '6 kuukauden kuluessa':
    max_date = min_date + timedelta(days=180)
else:  # 12 kuukauden kuluessa
    max_date = min_date + timedelta(days=365)

expiring_df = df[(df['legal_status_anticipated_term_date'] >= min_date) & (df['legal_status_anticipated_term_date'] <= max_date)]

unique_applicants = expiring_df['Hakija'].dropna().unique().tolist()
selected_applicant = st.selectbox('Valitse hakija:', unique_applicants)

filtered_df = expiring_df[expiring_df['Hakija'] == selected_applicant]
filtered_df = filtered_df.rename(columns={"invention_title": "Keksintö"})
filtered_df['legal_status_anticipated_term_date'] = filtered_df['legal_status_anticipated_term_date'].dt.strftime('%Y-%m-%d')
filtered_df['Link'] = "https://www.lens.org/lens/patent/" + filtered_df['lens_id'].astype(str)
filtered_df['Link'] = '<a href="' + filtered_df['Link'] + '" target="_blank">' + "Link" + '</a>'

st.write(f"Aktiiviset patentit hakijalta {selected_applicant} jotka erääntyvät seuraavan {option}:")
# Convert the DataFrame to an HTML table and display it using st.markdown
# Convert the DataFrame to an HTML table and display it using st.markdown
html_table = filtered_df[['publication_type', 'Keksintö', 'Hakija', 'legal_status_anticipated_term_date', 'Link']].to_html(escape=False, index=False)
st.markdown(html_table, unsafe_allow_html=True)


#st.write(filtered_df[['publication_type', 'Keksintö', 'Hakija', 'legal_status_anticipated_term_date', 'Link']], unsafe_allow_html=True)
#st.table(filtered_df[['publication_type', 'Keksintö', 'Hakija', 'legal_status_anticipated_term_date', 'Link']])
#st.write(f"Aktiiviset patentit hakijalta {selected_applicant} jotka erääntyvät seuraavan {option}:")
#st.table(filtered_df[['publication_type', 'invention_title', 'Hakija', 'legal_status_anticipated_term_date']])

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from queries import *

# Define a function to transform the text
def transform_text(text):
    if pd.isna(text):  
        return None
    return ' '.join([word.capitalize() for word in text.split()])

def render_mpl_table(data, col_width=3.0, row_height=0.625, font_size=12,
                     header_color='#40466e', row_colors=['#f1f1f2', 'w'], edge_color='w',
                     bbox=[0, 0, 1, 1], header_columns=0,
                     ax=None, **kwargs):
    if ax is None:
        size = (np.array(data.shape[::-1]) + np.array([0, 1])) * np.array([col_width, row_height])
        fig, ax = plt.subplots(figsize=size)
        ax.axis('off')

    mpl_table = ax.table(cellText=data.values, bbox=bbox, colLabels=data.columns, **kwargs)

    mpl_table.auto_set_font_size(False)
    mpl_table.set_fontsize(font_size)

    for k, cell in mpl_table._cells.items():
        cell.set_edgecolor(edge_color)
        if k[0] == 0 or k[1] < header_columns:
            cell.set_text_props(weight='bold', color='w')
            cell.set_facecolor(header_color)
        else:
            cell.set_facecolor(row_colors[k[0] % len(row_colors)])
    plt.show()

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
html_table = filtered_df[['publication_type', 'Keksintö', 'Hakija', 'legal_status_anticipated_term_date', 'Link']].to_html(escape=False, index=False)
st.markdown(html_table, unsafe_allow_html=True)


#st.write(filtered_df[['publication_type', 'Keksintö', 'Hakija', 'legal_status_anticipated_term_date', 'Link']], unsafe_allow_html=True)
#st.table(filtered_df[['publication_type', 'Keksintö', 'Hakija', 'legal_status_anticipated_term_date', 'Link']])
#st.write(f"Aktiiviset patentit hakijalta {selected_applicant} jotka erääntyvät seuraavan {option}:")
#st.table(filtered_df[['publication_type', 'invention_title', 'Hakija', 'legal_status_anticipated_term_date']])

def fetch_data(y_tunnus):
    # Define the SQL query
    query = """
    WITH Funding AS (
        SELECT 
            Y_tunnus,
            SUM(Toteutunut_EU_ja_valtion_rahoitus) as Total_Funding
        FROM 
            eura2020
        WHERE 
            Y_tunnus = ?
        GROUP BY 
            Y_tunnus
    ),
    DesignRights AS (
        SELECT 
            m.applicant_basename,
            COUNT(DISTINCT m.applicationNumber) as Design_Rights_Count
        FROM 
            mallioikeudet m
        JOIN 
            yritykset y ON y.yritys_basename = m.applicant_basename
        WHERE 
            y.y_tunnus = ?
        GROUP BY 
            m.applicant_basename
    ),
    Trademarks AS (
        SELECT 
            t.applicant_basename,
            COUNT(DISTINCT t.applicationNumber) as Trademarks_Count
        FROM 
            tavaramerkit t
        JOIN 
            yritykset y ON y.yritys_basename = t.applicant_basename
        WHERE 
            y.y_tunnus = ?
        GROUP BY 
            t.applicant_basename
    ),
    Patents AS (
        SELECT 
            p.applicant_basename,
            COUNT(DISTINCT p.lens_id) as Patent_Applications_Count
        FROM 
            applicants p
        JOIN 
            yritykset y ON y.yritys_basename = p.applicant_basename
        WHERE 
            y.y_tunnus = ?
        GROUP BY 
            p.applicant_basename
    ),
    EUHorizon AS (
    SELECT 
        beneficiary_basename,
        SUM([Beneficiary’s contracted amount (EUR)]) as Total_EU_Horizon_Funding
    FROM 
        EU_Horizon

    JOIN yritykset y on y.yritys_basename = EU_Horizon.beneficiary_basename

    WHERE 
        y.y_tunnus = ?
    GROUP BY 
        EU_Horizon.beneficiary_basename
    ),
    BusinessFinland AS (
    SELECT 
        Business_Finland.Y_tunnus,
        SUM(CAST(Avustus as FLOAT)) as Total_Business_Finland_Funding
    FROM 
        Business_Finland

    JOIN yritykset y on y.y_tunnus = Business_Finland.Y_tunnus
    WHERE 
        y.y_tunnus = ?
    GROUP BY 
        Business_Finland.Y_tunnus
    )

    SELECT 
    y.y_tunnus,
    y.yritys,
    y.yritys_basename,
    COALESCE(f.Total_Funding, 0) as Total_Funding,
    COALESCE(d.Design_Rights_Count, 0) as Design_Rights_Count,
    COALESCE(t.Trademarks_Count, 0) as Trademarks_Count,
    COALESCE(p.Patent_Applications_Count, 0) as Patent_Applications_Count,
    COALESCE(eh.Total_EU_Horizon_Funding, 0) as Total_EU_Horizon_Funding,
    COALESCE(bf.Total_Business_Finland_Funding, 0) as Total_Business_Finland_Funding
    FROM 
    yritykset y
    LEFT JOIN 
    Funding f ON y.y_tunnus = f.Y_tunnus
    LEFT JOIN 
    DesignRights d ON y.yritys_basename = d.applicant_basename
    LEFT JOIN 
    Trademarks t ON y.yritys_basename = t.applicant_basename
    LEFT JOIN 
    Patents p ON y.yritys_basename = p.applicant_basename
    LEFT JOIN 
    EUHorizon eh ON y.yritys_basename = eh.beneficiary_basename
    LEFT JOIN 
    BusinessFinland bf ON y.y_tunnus = bf.Y_tunnus
    WHERE 
    y.y_tunnus = ?;
    """
    
    # Connect to the database and fetch the data into a Pandas DataFrame
    with pyodbc.connect(f'DRIVER={driver};SERVER={server};PORT=1433;DATABASE={database};UID={username};PWD={password}') as conn:
        df = pd.read_sql(query, conn, params=(y_tunnus, y_tunnus, y_tunnus, y_tunnus, y_tunnus, y_tunnus,y_tunnus))
        
    return df
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

# Inject custom styles into the app
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
    #st.write("Debug: Fetched data:")
    #st.write(data)

    if not data.empty:
        st.markdown(f"<div class='large-font'>{data['yritys'].iloc[0]}</div>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)  # Create two columns
    
        # Content for the first column
        # Content for the first column
        card_content1 = f"""
        <div style="background-color: #f5f5f5; padding: 15px; border-radius: 5px;">
        <div class="medium-font">EURA-rahoitus päätoteuttajana</div>
        <div class="large-number">{int(data['Total_Funding'].iloc[0]):,} €</div>
        <div class="small-font"><a href="/detailed_info?y_tunnus={y_tunnus}&type=Total_Funding">linkki tarkempiin tietoihin (esim. isoimmat hankkeet)</a></div>
        <hr>
        <div class="medium-font">EU Horizon tuet</div>
        <div class="large-number">{int(data['Total_EU_Horizon_Funding'].iloc[0]):,}</div>
        <div class="small-font"><a href="/detailed_info?y_tunnus={y_tunnus}&type=Total_EU_Horizon_Funding">linkki tarkempiin tietoihin (hankkeet ja ohjelmat)</a></div>
        <hr>
        <div class="medium-font">Business Finland tuet</div>
        <div class="large-number">{int(data['Total_Business_Finland_Funding'].iloc[0]):,}</div>
        <div class="small-font"><a href="/detailed_info?y_tunnus={y_tunnus}&type=Total_Business_Finland_Funding">linkki tarkempiin tietoihin</a></div>
        </div>
        """
        col1.markdown(card_content1, unsafe_allow_html=True)

        # Content for the second column
        card_content2 = f"""
        <div style="background-color: #f5f5f5; padding: 15px; border-radius: 5px;">
        <div class="medium-font">Patenttien määrä</div>
        <div class="large-number">{int(data['Patent_Applications_Count'].iloc[0]):,}</div>
        <div class="small-font"><a href="/detailed_info?y_tunnus={y_tunnus}&type=Patent_Applications_Count">linkki tarkempiin tietoihin (patenttilistaus + visualisoinnit)</a></div>
        <hr>
        <div class="medium-font">Tavaramerkkien määrä</div>
        <div class="large-number">{int(data['Trademarks_Count'].iloc[0]):,}</div>
        <div class="small-font"><a href="/detailed_info?y_tunnus={y_tunnus}&type=Trademarks_Count">linkki tarkempiin tietoihin (sanat & kuvat?)</a></div>
        <hr>
        <div class="medium-font">Mallioikeuksien määrä</div>
        <div class="large-number">{int(data['Design_Rights_Count'].iloc[0]):,}</div>
        <div class="small-font"><a href="/detailed_info?y_tunnus={y_tunnus}&type=Design_Rights_Count">linkki tarkempiin tietoihin</a></div>
        </div>
        """
        col2.markdown(card_content2, unsafe_allow_html=True)


    else:
        st.write("Dataa ei löytynyt :(")

import streamlit as st

# Your existing style and other setup code...

# Get query parameters
page_type = st.experimental_get_query_params().get("type", [""])[0]
y_tunnus_param = st.experimental_get_query_params().get("y_tunnus", [""])[0]

if page_type and y_tunnus_param:
    st.title(f"Displaying detailed data for {page_type}")


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
    #st.write("Debug: Fetched data:")
    #st.write(data)

    if not data.empty:
        st.markdown(f"<div class='large-font'>{data['yritys'].iloc[0]}</div>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)  # Create two columns
    
        # Content for the first column
        # Content for the first column
        card_content1 = f"""
        <div style="background-color: #f5f5f5; padding: 15px; border-radius: 5px;">
        <div class="medium-font">EU Horizon rahoitus 2013-2030</div>
        <div class="large-number">{int(data['Total_EU_Horizon_Funding'].iloc[0]):,}</div>
        <div class="small-font"><a href="/detailed_info?y_tunnus={y_tunnus}&type=Total_EU_Horizon_Funding">linkki tarkempiin tietoihin (hankkeet ja ohjelmat)</a></div>
        <hr>
        <div class="medium-font">EURA-rahoitus 2014-2020 ohjelmakausi</div>
        <div class="large-number">{int(data['Total_Funding'].iloc[0]):,} €</div>
        <div class="small-font">2021-2027 ohjelmakauden tietolähde julkaistaan lokakuun alussa</div>
        <div class="small-font"><a href="/detailed_info?y_tunnus={y_tunnus}&type=Total_Funding">linkki tarkempiin tietoihin (esim. isoimmat hankkeet)</a></div>
        <hr>
        <div class="medium-font">Business Finland tuet</div>
        <div class="large-number">{int(data['Total_Business_Finland_Funding'].iloc[0]):,}</div>
        <div class="small-font"><a href="/detailed_info?y_tunnus={y_tunnus}&type=Total_Business_Finland_Funding">linkki tarkempiin tietoihin</a></div>
        </div>
        """
        col1.markdown(card_content1, unsafe_allow_html=True)

        # Content for the second column
        card_content2 = f"""
        <div style="background-color: #f5f5f5; padding: 15px; border-radius: 5px;">
        <div class="medium-font">Patenttien määrä</div>
        <div class="large-number">{int(data['Patent_Applications_Count'].iloc[0]):,}</div>
        <div class="small-font"><a href="/detailed_info?y_tunnus={y_tunnus}&type=Patent_Applications_Count">linkki tarkempiin tietoihin (patenttilistaus + visualisoinnit)</a></div>
        <hr>
        <div class="medium-font">Tavaramerkkien määrä</div>
        <div class="large-number">{int(data['Trademarks_Count'].iloc[0]):,}</div>
        <div class="small-font"><a href="/detailed_info?y_tunnus={y_tunnus}&type=Trademarks_Count">linkki tarkempiin tietoihin (sanat & kuvat?)</a></div>
        <hr>
        <div class="medium-font">Mallioikeuksien määrä</div>
        <div class="large-number">{int(data['Design_Rights_Count'].iloc[0]):,}</div>
        <div class="small-font"><a href="/detailed_info?y_tunnus={y_tunnus}&type=Design_Rights_Count">linkki tarkempiin tietoihin</a></div>
        </div>
        """
        col2.markdown(card_content2, unsafe_allow_html=True)


    else:
        st.write("Dataa ei löytynyt :(")

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
        <div class="small-font"><a href="/detailed_info?y_tunnus={y_tunnus}&type=Total_EU_Horizon_Funding">linkki tarkempiin tietoihin (hankkeet ja ohjelmat)</a></div>
        <hr>
        <div class="medium-font">EURA-rahoitus 2014-2020 ohjelmakausi</div>
        <div class="large-number">{format_currency(int(data['Total_Funding'].iloc[0]))}</div>
        <div class="small-font">2021-2027 ohjelmakauden tietolähde julkaistaan lokakuun alussa</div>
        <div class="small-font"><a href="/detailed_info?y_tunnus={y_tunnus}&type=Total_Funding">linkki tarkempiin tietoihin (esim. isoimmat hankkeet)</a></div>
        <hr>
        <div class="medium-font">Business Finland tuet</div>
        <div class="large-number">{format_currency(int(data['Total_Business_Finland_Funding'].iloc[0]))}</div>
        <div class="small-font"><a href="/detailed_info?y_tunnus={y_tunnus}&type=Total_Business_Finland_Funding">linkki tarkempiin tietoihin</a></div>
        </div>
        """
        col1.markdown(card_content1, unsafe_allow_html=True)

        # Content for the second column
        card_content2 = f"""
        <div style="background-color: #f5f5f5; padding: 15px; border-radius: 5px;">
        <div class="medium-font">Patenttien määrä</div>
        <div class="large-number">{int(data['Patent_Applications_Count'].iloc[0]):,}</div>
        <div class="small-font"><a href="/detailed_info?y_tunnus={y_tunnus}&type=Patent_Applications_Count">linkki tarkempiin tietoihin (patenttilistaus + visualisoinnit)</a></div>
        <hr>
        <div class="medium-font">Tavaramerkkien määrä</div>
        <div class="large-number">{int(data['Trademarks_Count'].iloc[0]):,}</div>
        <div class="small-font"><a href="/detailed_info?y_tunnus={y_tunnus}&type=Trademarks_Count">linkki tarkempiin tietoihin (sanat & kuvat?)</a></div>
        <hr>
        <div class="medium-font">Mallioikeuksien määrä</div>
        <div class="large-number">{int(data['Design_Rights_Count'].iloc[0]):,}</div>
        <div class="small-font"><a href="/detailed_info?y_tunnus={y_tunnus}&type=Design_Rights_Count">linkki tarkempiin tietoihin</a></div>
        </div>
        """
        col2.markdown(card_content2, unsafe_allow_html=True)

    else:
        st.write("Dataa ei löytynyt :(")

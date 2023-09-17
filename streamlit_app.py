import pandas as pd
import pyodbc
import streamlit as st

driver = st.secrets["driver"]
server = st.secrets["server"]
database = st.secrets["database"]
username = st.secrets["username"]
password = st.secrets["password"]

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
    )

    SELECT 
        y.y_tunnus,
        y.yritys,
        y.yritys_basename,
        COALESCE(f.Total_Funding, 0) as Total_Funding,
        COALESCE(d.Design_Rights_Count, 0) as Design_Rights_Count,
        COALESCE(t.Trademarks_Count, 0) as Trademarks_Count,
        COALESCE(p.Patent_Applications_Count, 0) as Patent_Applications_Count
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
    WHERE 
        y.y_tunnus = ?;
    """
    
    # Connect to the database and fetch the data into a Pandas DataFrame
    with pyodbc.connect(f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={db_info['server']};PORT=1433;DATABASE={db_info['database']};UID={db_info['username']};PWD={db_info['password']}") as conn:
        df = pd.read_sql(query, conn, params=(y_tunnus, y_tunnus, y_tunnus, y_tunnus, y_tunnus))

        
    return df

st.sidebar.text("sivubaarin teksti")

st.title('Hae rahoitustiedot')

# Input for Y_tunnus
y_tunnus = st.text_input("Anna Y-tunnus (ja paina enter)")

# If a Y_tunnus is given, fetch and display the data
if y_tunnus:
    data = fetch_data(y_tunnus)
    st.write("Debug: Fetched data:")
    st.write(data)

    if not data.empty:
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.subheader("Y-tunnus")
            st.write(data['y_tunnus'].iloc[0])

        with col2:
            st.subheader("Yritys")
            st.write(data['yritys'].iloc[0])

        # Displaying Design Rights Count
        with col3:
            st.subheader("Design Rights Count")
            st.write(data['Design_Rights_Count'].iloc[0]) 

        # Displaying Trademarks Count
        with col4:
            st.subheader("Trademarks Count")
            st.write(data['Trademarks_Count'].iloc[0])

        # Card display below columns
        card_style = """
        background-color: #f5f5f5;
        padding: 15px;
        border-radius: 5px;
        """
        
        st.markdown(f"""
        <div style='{card_style}'>
            <h4>Saadut EU-rahoitukset</h4>
            <p>EURA 2014-2020: {data['Total_Funding'].iloc[0]} €</p>
            <h4>Patent Applications Count</h4>
            <p>{data['Patent_Applications_Count'].iloc[0]}</p>
        </div>
        """, unsafe_allow_html=True)

    else:
        st.write("Dataa ei löytynyt :(")

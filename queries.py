import pyodbc
import streamlit as st
import pandas as pd

driver = st.secrets["driver"]
server = st.secrets["server"]
database = st.secrets["database"]
username = st.secrets["username"]
password = st.secrets["password"]

def fetch_data(y_tunnus):
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
            yritykset y ON y.yritys_basename2 = p.applicant_basename
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

    JOIN yritykset y on y.yritys_basename2 = EU_Horizon.beneficiary_basename

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
    y.yritys_basename2,
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
    Patents p ON y.yritys_basename2 = p.applicant_basename
    LEFT JOIN 
    EUHorizon eh ON y.yritys_basename2 = eh.beneficiary_basename
    LEFT JOIN 
    BusinessFinland bf ON y.y_tunnus = bf.Y_tunnus
    WHERE 
    y.y_tunnus = ?;
    """
    
    with pyodbc.connect(f'DRIVER={driver};SERVER={server};PORT=1433;DATABASE={database};UID={username};PWD={password}') as conn:
        df = pd.read_sql(query, conn, params=(y_tunnus, y_tunnus, y_tunnus, y_tunnus, y_tunnus, y_tunnus, y_tunnus))
        
    return df


def fetch_horizon_data(y_tunnus):
    query = """SELECT * FROM EU_Horizon2 WHERE y_tunnus = ?;"""
    
    with pyodbc.connect(f'DRIVER={driver};SERVER={server};PORT=1433;DATABASE={database};UID={username};PWD={password}') as conn:
        df = pd.read_sql(query, conn, params=(y_tunnus,))
    return df
    
def fetch_eura_data(y_tunnus):
    query = """SELECT * FROM EURA2020 WHERE Y_tunnus = ?;"""
    
    with pyodbc.connect(f'DRIVER={driver};SERVER={server};PORT=1433;DATABASE={database};UID={username};PWD={password}') as conn:
        df = pd.read_sql(query, conn, params=(y_tunnus,))
    return df
    
@st.cache_data
def fetch_legal_status_data():
    query = """
    SELECT 
        p.lens_id, 
        p.invention_title, 
        p.legal_status_anticipated_term_date,
        p.publication_type,
        a.extracted_name,
        a.applicant_basename,
        y.yritys,
        y.yhtiömuoto,
        y.y_tunnus
    FROM patents p
    LEFT JOIN applicants a ON p.lens_id = a.lens_id
    LEFT JOIN yritykset y ON a.applicant_basename = y.yritys_basename2
    WHERE p.legal_status_patent_status IS NOT NULL
    ORDER BY p.legal_status_anticipated_term_date ASC;
    """
    
    with pyodbc.connect(f'DRIVER={driver};SERVER={server};PORT=1433;DATABASE={database};UID={username};PWD={password}') as conn:
        df = pd.read_sql(query, conn)
    return df

@st.cache_data()
def fetch_aggregated_data():
    query = """
    WITH 
    Funding AS (
        SELECT 
            Y_tunnus,
            SUM(Toteutunut_EU_ja_valtion_rahoitus) as Total_Funding
        FROM 
            eura2020
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
            yritykset y ON y.yritys_basename2 = p.applicant_basename
        GROUP BY 
            p.applicant_basename
    ),
    EUHorizon AS (
        SELECT 
            beneficiary_basename,
            SUM([Beneficiary’s contracted amount (EUR)]) as Total_EU_Horizon_Funding
        FROM 
            EU_Horizon
        JOIN 
            yritykset y on y.yritys_basename2 = EU_Horizon.beneficiary_basename
        GROUP BY 
            EU_Horizon.beneficiary_basename
    ),
    BusinessFinland AS (
        SELECT 
            Business_Finland.Y_tunnus,
            SUM(CAST(Avustus as FLOAT)) as Total_Business_Finland_Funding,
            SUM(CAST(Tutkimusrahoitus as FLOAT)) as Total_Tutkimusrahoitus
        FROM 
            Business_Finland
        JOIN 
            yritykset y on y.y_tunnus = Business_Finland.Y_tunnus
        GROUP BY 
            Business_Finland.Y_tunnus
    ),
    PostinumeroInfo AS (
        SELECT 
            Postinumeroalue,
            Maakunnan_nimi
        FROM 
            Postinumeroalueet
    )
    SELECT 
        y.y_tunnus,
        y.yritys,
        y.yritys_basename2,
        y.postinumero,
        y.yrityksen_rekisteröimispäivä,
        y.toimiala,
        y.päätoimiala,
        y.yhtiömuoto,
        y.status,
        COALESCE(f.Total_Funding, 0) as Total_Funding,
        COALESCE(d.Design_Rights_Count, 0) as Design_Rights_Count,
        COALESCE(t.Trademarks_Count, 0) as Trademarks_Count,
        COALESCE(p.Patent_Applications_Count, 0) as Patent_Applications_Count,
        COALESCE(eh.Total_EU_Horizon_Funding, 0) as Total_EU_Horizon_Funding,
        COALESCE(bf.Total_Business_Finland_Funding, 0) as Total_Business_Finland_Funding,
        COALESCE(bf.Total_Tutkimusrahoitus, 0) as Total_Tutkimusrahoitus,
        pi.Maakunnan_nimi
    FROM 
        yritykset y
    LEFT JOIN 
        Funding f ON y.y_tunnus = f.Y_tunnus
    LEFT JOIN 
        DesignRights d ON y.yritys_basename = d.applicant_basename
    LEFT JOIN 
        Trademarks t ON y.yritys_basename = t.applicant_basename
    LEFT JOIN 
        Patents p ON y.yritys_basename2 = p.applicant_basename
    LEFT JOIN 
        EUHorizon eh ON y.yritys_basename2 = eh.beneficiary_basename
    LEFT JOIN 
        BusinessFinland bf ON y.y_tunnus = bf.Y_tunnus
    LEFT JOIN 
        PostinumeroInfo pi ON 
        CASE 
            WHEN RIGHT(y.postinumero, 1) = '1' THEN LEFT(y.postinumero, LEN(y.postinumero) - 1) + '0'
            ELSE y.postinumero
        END 
        = pi.Postinumeroalue
    WHERE 
        COALESCE(f.Total_Funding, 0) <> 0 OR
        COALESCE(d.Design_Rights_Count, 0) <> 0 OR
        COALESCE(t.Trademarks_Count, 0) <> 0 OR
        COALESCE(p.Patent_Applications_Count, 0) <> 0 OR
        COALESCE(eh.Total_EU_Horizon_Funding, 0) <> 0 OR
        COALESCE(bf.Total_Business_Finland_Funding, 0) <> 0 OR
        COALESCE(bf.Total_Tutkimusrahoitus, 0) <> 0;
    """
    
    with pyodbc.connect(f'DRIVER={driver};SERVER={server};PORT=1433;DATABASE={database};UID={username};PWD={password}') as conn:
        df = pd.read_sql(query, conn)
    return df
    
@st.cache_data
def fetch_collaboration_data():
    query = """
    SELECT 
        c.FinnishOrgId, 
        c.FinnishOrgName, 
        c.CollaboratorOrgId, 
        c.CollaboratorOrgName, 
        c.CollaboratorCountry,
        c.ProjectId, 
        c.ProjectTitle,
        c.FinnishOrgContribution,
        c.ProjectRole,
        c.StartDate,
        c.EndDate,
        s.euroSciVocTitle
    FROM 
        horizon_collaborations c
    LEFT JOIN 
        horizon_europe_SciVoc s ON c.ProjectId = s.projectId;
    """
    with pyodbc.connect(f'DRIVER={driver};SERVER={server};PORT=1433;DATABASE={database};UID={username};PWD={password}') as conn:
        df = pd.read_sql(query, conn)
        
    return df

import pyodbc
import pandas as pd

def fetch_data2(y_tunnus):
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
            yritykset y ON y.yritys_basename2 = p.applicant_basename
        WHERE 
            y.y_tunnus = ?
        GROUP BY 
            p.applicant_basename
    ),
    EUHorizon AS (
        SELECT 
            y_tunnus,
            SUM([Beneficiary’s contracted amount (EUR)]) as Total_EU_Horizon_Funding
        FROM 
            EU_Horizon2
        WHERE 
            y_tunnus = ?
        GROUP BY 
            y_tunnus
    ),
    BusinessFinland AS (
        SELECT 
            Business_Finland.Y_tunnus,
            SUM(CAST(Avustus as FLOAT)) as Total_Business_Finland_Funding,
            SUM(CAST(Tutkimusrahoitus as FLOAT)) as Total_Tutkimusrahoitus  -- Sum the Tutkimusrahoitus column
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
        y.yritys_basename2,
        COALESCE(f.Total_Funding, 0) as Total_Funding,
        COALESCE(d.Design_Rights_Count, 0) as Design_Rights_Count,
        COALESCE(t.Trademarks_Count, 0) as Trademarks_Count,
        COALESCE(p.Patent_Applications_Count, 0) as Patent_Applications_Count,
        COALESCE(eh.Total_EU_Horizon_Funding, 0) as Total_EU_Horizon_Funding,
        COALESCE(bf.Total_Business_Finland_Funding, 0) as Total_Business_Finland_Funding,
        COALESCE(bf.Total_Tutkimusrahoitus, 0) as Total_Tutkimusrahoitus  -- Add Total_Tutkimusrahoitus to the SELECT
    FROM 
        yritykset y
    LEFT JOIN 
        Funding f ON y.y_tunnus = f.Y_tunnus
    LEFT JOIN 
        DesignRights d ON y.yritys_basename = d.applicant_basename
    LEFT JOIN 
        Trademarks t ON y.yritys_basename = t.applicant_basename
    LEFT JOIN 
        Patents p ON y.yritys_basename2 = p.applicant_basename
    LEFT JOIN 
        EUHorizon eh ON y.y_tunnus = eh.y_tunnus
    LEFT JOIN 
        BusinessFinland bf ON y.y_tunnus = bf.Y_tunnus
    WHERE 
        y.y_tunnus = ?;
    """
    
    with pyodbc.connect(f'DRIVER={driver};SERVER={server};PORT=1433;DATABASE={database};UID={username};PWD={password}') as conn:
           df = pd.read_sql(query, conn, params=(y_tunnus, y_tunnus, y_tunnus, y_tunnus, y_tunnus, y_tunnus, y_tunnus))
        
    return df
    
def fetch_individual_data(y_tunnus):
    query = """
    SELECT 
        y.y_tunnus,
        y.yritys,
        y.yritys_basename2,
        e.Toteutunut_EU_ja_valtion_rahoitus,
        m.applicationNumber AS DesignRights_ApplicationNumber,
        t.applicationNumber AS Trademarks_ApplicationNumber,
        p.lens_id AS Patent_Applications_Lens_Id,
        EU_Horizon.[Beneficiary’s contracted amount (EUR)],
        CAST(Business_Finland.Avustus as FLOAT) as Business_Finland_Funding
    FROM 
        yritykset y
    LEFT JOIN 
        eura2020 e ON y.y_tunnus = e.Y_tunnus AND y.y_tunnus = ?
    LEFT JOIN 
        mallioikeudet m ON y.yritys_basename = m.applicant_basename AND y.y_tunnus = ?
    LEFT JOIN 
        tavaramerkit t ON y.yritys_basename = t.applicant_basename AND y.y_tunnus = ?
    LEFT JOIN 
        applicants p ON y.yritys_basename2 = p.applicant_basename AND y.y_tunnus = ?
    LEFT JOIN 
        EU_Horizon ON y.yritys_basename2 = EU_Horizon.beneficiary_basename AND y.y_tunnus = ?
    LEFT JOIN 
        Business_Finland ON y.y_tunnus = Business_Finland.Y_tunnus AND y.y_tunnus = ?
    """
    
    with pyodbc.connect(f'DRIVER={driver};SERVER={server};PORT=1433;DATABASE={database};UID={username};PWD={password}') as conn:
        df = pd.read_sql(query, conn, params=(y_tunnus, y_tunnus, y_tunnus, y_tunnus, y_tunnus, y_tunnus))
        
    return df
    
@st.cache_data
def get_company_names():
    query = "SELECT DISTINCT yritys FROM yritykset ORDER BY yritys;"
    with pyodbc.connect(f'DRIVER={driver};SERVER={server};PORT=1433;DATABASE={database};UID={username};PWD={password}') as conn:
        df = pd.read_sql(query, conn)
    return df['yritys'].tolist()

def fetch_data3(yritys_name):
    # Define the SQL query
    query = """
    WITH Funding AS (
        SELECT 
            y.yritys,
            SUM(Toteutunut_EU_ja_valtion_rahoitus) as Total_Funding
        FROM 
            eura2020
        JOIN 
            yritykset y ON y.y_tunnus = eura2020.Y_tunnus
        WHERE 
            y.yritys = ?
        GROUP BY 
            y.yritys
    ),
    DesignRights AS (
        SELECT 
            y.yritys,
            COUNT(DISTINCT m.applicationNumber) as Design_Rights_Count
        FROM 
            mallioikeudet m
        JOIN 
            yritykset y ON y.yritys_basename = m.applicant_basename
        WHERE 
            y.yritys = ?
        GROUP BY 
            y.yritys
    ),
    Trademarks AS (
        SELECT 
            y.yritys,
            COUNT(DISTINCT t.applicationNumber) as Trademarks_Count
        FROM 
            tavaramerkit t
        JOIN 
            yritykset y ON y.yritys_basename = t.applicant_basename
        WHERE 
            y.yritys = ?
        GROUP BY 
            y.yritys
    ),
    Patents AS (
        SELECT 
            y.yritys,
            COUNT(DISTINCT p.lens_id) as Patent_Applications_Count
        FROM 
            applicants p
        JOIN 
            yritykset y ON y.yritys_basename2 = p.applicant_basename
        WHERE 
            y.yritys = ?
        GROUP BY 
            y.yritys
    ),
    EUHorizon AS (
        SELECT 
            y.yritys,
            SUM([Beneficiary’s contracted amount (EUR)]) as Total_EU_Horizon_Funding
        FROM 
            EU_Horizon
        JOIN yritykset y on y.yritys_basename2 = EU_Horizon.beneficiary_basename
        WHERE 
            y.yritys = ?
        GROUP BY 
            y.yritys
    ),
    BusinessFinland AS (
        SELECT 
            y.yritys,
            SUM(CAST(Avustus as FLOAT)) as Total_Business_Finland_Funding,
            SUM(CAST(Tutkimusrahoitus as FLOAT)) as Total_Tutkimusrahoitus
        FROM 
            Business_Finland
        JOIN yritykset y on y.y_tunnus = Business_Finland.Y_tunnus
        WHERE 
            y.yritys = ?
        GROUP BY 
            y.yritys
    )

    SELECT 
        y.y_tunnus,
        y.yritys,
        y.yritys_basename2,
        COALESCE(f.Total_Funding, 0) as Total_Funding,
        COALESCE(d.Design_Rights_Count, 0) as Design_Rights_Count,
        COALESCE(t.Trademarks_Count, 0) as Trademarks_Count,
        COALESCE(p.Patent_Applications_Count, 0) as Patent_Applications_Count,
        COALESCE(eh.Total_EU_Horizon_Funding, 0) as Total_EU_Horizon_Funding,
        COALESCE(bf.Total_Business_Finland_Funding, 0) as Total_Business_Finland_Funding,
        COALESCE(bf.Total_Tutkimusrahoitus, 0) as Total_Tutkimusrahoitus
    FROM 
        yritykset y
    LEFT JOIN 
        Funding f ON y.yritys = f.yritys
    LEFT JOIN 
        DesignRights d ON y.yritys = d.yritys
    LEFT JOIN 
        Trademarks t ON y.yritys = t.yritys
    LEFT JOIN 
        Patents p ON y.yritys = p.yritys
    LEFT JOIN 
        EUHorizon eh ON y.yritys = eh.yritys
    LEFT JOIN 
        BusinessFinland bf ON y.yritys = bf.yritys
    WHERE 
        y.yritys = ?;
    """
    
    with pyodbc.connect(f'DRIVER={driver};SERVER={server};PORT=1433;DATABASE={database};UID={username};PWD={password}') as conn:
        df = pd.read_sql(query, conn, params=(yritys_name,)*7)  # Adjust the number of parameters as needed
        
    return df

def fetch_company_data(y_tunnus):
    query = """
    SELECT y.y_tunnus,
    y.yritys,
    p.date_published,
    p.publication_type,
    p.legal_status_patent_status,
    t.applicationDate
    FROM yritykset y
    LEFT JOIN applicants a ON y.yritys_basename = a.applicant_basename
    LEFT JOIN patents p ON a.lens_id = p.lens_id
    LEFT JOIN tavaramerkit t ON y.yritys_basename = t.applicant_basename
    WHERE y.y_tunnus = ?
    """
    with pyodbc.connect(f'DRIVER={driver};SERVER={server};PORT=1433;DATABASE={database};UID={username};PWD={password}') as conn:
        df = pd.read_sql(query, conn, params=(y_tunnus,))
    return df

def fetch_time_series_data(y_tunnus):
    patents_query = """
    SELECT y.y_tunnus,
           y.yritys,
           p.date_published,
           p.publication_type,
           p.legal_status_patent_status
    FROM yritykset y
    LEFT JOIN applicants a ON y.yritys_basename2 = a.applicant_basename
    LEFT JOIN patents p ON a.lens_id = p.lens_id
    WHERE y.y_tunnus = ? AND p.date_published IS NOT NULL
    """

    # Trademarks query
    trademarks_query = """
    SELECT y.y_tunnus,
           y.yritys,
           t.applicationDate
    FROM yritykset y
    LEFT JOIN tavaramerkit t ON y.yritys_basename = t.applicant_basename
    WHERE y.y_tunnus = ? AND t.applicationDate IS NOT NULL
    """
    
    with pyodbc.connect(f'DRIVER={driver};SERVER={server};PORT=1433;DATABASE={database};UID={username};PWD={password}') as conn:
        patents_df = pd.read_sql_query(patents_query, conn, params=(y_tunnus,))
        trademarks_df = pd.read_sql_query(trademarks_query, conn, params=(y_tunnus,))

    return patents_df, trademarks_df

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
    with pyodbc.connect(f'DRIVER={driver};SERVER={server};PORT=1433;DATABASE={database};UID={username};PWD={password}') as conn:
        df = pd.read_sql(query, conn, params=(y_tunnus, y_tunnus, y_tunnus, y_tunnus, y_tunnus))
        
    return df

WITH Funding AS (
        SELECT 
            Y_tunnus,
            SUM(Toteutunut_EU_ja_valtion_rahoitus) as Total_Funding
        FROM 
            eura2020
        WHERE 
            Y_tunnus = '2472908-2'
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
            y.y_tunnus = '2472908-2'
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
            y.y_tunnus = '2472908-2'
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
            y.y_tunnus = '2472908-2'
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
        y.y_tunnus = '2472908-2'
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
        y.y_tunnus = '2472908-2'
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
    y.y_tunnus = '2472908-2';

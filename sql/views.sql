CREATE VIEW county_health_summary AS
SELECT
    fips,
    county_name,
    population,
    poverty_rate,
    diabetes,
    obesity,
    inactivity,
    smoking,
    mental_health,
    hpsa_score,
    shortage_flag
FROM county_health;

CREATE VIEW high_risk_counties AS
SELECT *
FROM county_health
WHERE
    poverty_rate > 20
    OR diabetes > 15
    OR hpsa_score > 18;

CREATE VIEW shortage_analysis AS
SELECT
    shortage_flag,
    AVG(diabetes) AS avg_diabetes,
    AVG(obesity) AS avg_obesity,
    AVG(poverty_rate) AS avg_poverty
FROM county_health
GROUP BY shortage_flag;


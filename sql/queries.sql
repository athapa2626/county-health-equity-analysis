-- 1. Highest poverty counties in the U.S.
SELECT
    county_name,
    poverty_rate,
    population
FROM county_health
ORDER BY poverty_rate DESC
LIMIT 20;

-- 2. Counties with highest diabetes prevalence
SELECT
    county_name,
    diabetes,
    obesity,
    inactivity
FROM county_health
ORDER BY diabetes DESC
LIMIT 20;

-- 3. Relationship between poverty and obesity rates
SELECT
    county_name,
    poverty_rate,
    obesity
FROM county_health
WHERE poverty_rate IS NOT NULL
  AND obesity IS NOT NULL
ORDER BY poverty_rate DESC;

-- 4. High shortage (low access) counties
SELECT
    county_name,
    hpsa_score,
    diabetes
FROM county_health
WHERE hpsa_score IS NOT NULL
ORDER BY hpsa_score DESC;

-- 5. Counties designated as healthcare shortage areas
SELECT
    county_name,
    shortage_flag,
    hpsa_score,
    obesity,
    diabetes
FROM county_health
WHERE shortage_flag = 1;

-- 6. ER utilization and chronic disease burden
SELECT
    county_name,
    benes_total_cnt,
    benes_er_visits_cnt,
    diabetes,
    obesity
FROM county_health
ORDER BY benes_er_visits_cnt DESC;

-- 7. Highest ER utilization counties
SELECT
    county_name,
    benes_er_visits_cnt,
    benes_ip_cvrd_stay_cnt
FROM county_health
ORDER BY benes_er_visits_cnt DESC
LIMIT 25;

-- 8. Top Medicare beneficiary counties
SELECT
    county_name,
    hpsa_score,
    benes_total_cnt,
    benes_er_visits_cnt
FROM county_health
WHERE hpsa_score IS NOT NULL
ORDER BY hpsa_score DESC;

-- 9. Healthcare access vs Medicare utilization
SELECT
    county_name,
    poverty_rate,
    benes_er_visits_cnt,
    benes_ip_cvrd_stay_cnt
FROM county_health
WHERE poverty_rate > 15
ORDER BY benes_er_visits_cnt DESC;

-- 10. High poverty + high hospitalization burden
SELECT
    shortage_flag,
    AVG(diabetes) AS avg_diabetes,
    AVG(obesity) AS avg_obesity,
    AVG(poverty_rate) AS avg_poverty
FROM county_health
GROUP BY shortage_flag;

-- 11. Average health outcomes by shortage status
SELECT
    county_name,
    obesity,
    hpsa_score
FROM county_health
WHERE obesity > 40
ORDER BY hpsa_score DESC;

-- 12. Extreme obesity counties vs healthcare access
SELECT
    county_name,
    benes_total_cnt,
    benes_er_visits_cnt,
    benes_op_cnt
FROM county_health
ORDER BY benes_total_cnt DESC
LIMIT 20;
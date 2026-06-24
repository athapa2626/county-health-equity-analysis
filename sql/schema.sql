CREATE TABLE county_health (
    fips TEXT PRIMARY KEY,
    county_name TEXT,
    population INTEGER,
    median_income INTEGER,

    poverty_count INTEGER,
    poverty_universe INTEGER,
    poverty_rate REAL,

    diabetes REAL,
    obesity REAL,
    inactivity REAL,
    smoking REAL,
    mental_health REAL,

    hpsa_score REAL,
    hpsa_score_norm REAL,
    shortage_flag INTEGER,

    benes_total_cnt REAL,
    benes_ma_cnt REAL,
    ma_prtctn_rate REAL,

    benes_ip_cvrd_stay_cnt REAL,
    benes_er_visits_cnt REAL,
    benes_op_cnt REAL,

    benes_snf_cnt REAL,
    benes_hh_cnt REAL,
    benes_amblnc_cnt REAL
);
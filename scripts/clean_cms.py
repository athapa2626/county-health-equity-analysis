import pandas as pd
import zipfile
from pathlib import Path

# ----------------------------
# PATHS
# ----------------------------
project_root = Path(__file__).resolve().parents[1]
raw_path = project_root / "data" / "raw" / "cms_raw.csv"
clean_path = project_root / "data" / "clean" / "cms_clean.csv"

clean_path.parent.mkdir(parents=True, exist_ok=True)

# ----------------------------
# LOAD DATA (ZIP FILE)
# ----------------------------
with zipfile.ZipFile(raw_path, 'r') as z:
    csv_file = [f for f in z.namelist() if f.endswith(".csv")][0]
    with z.open(csv_file) as f:
        df = pd.read_csv(f, low_memory=False)

print("Raw shape:", df.shape)

# ----------------------------
# STEP 1: KEEP COUNTY ONLY
# ----------------------------
df = df[df["BENE_GEO_LVL"].astype(str).str.lower() == "county"].copy()

print("After county filter:", df.shape)

# ----------------------------
# STEP 2: CLEAN FIPS
# ----------------------------
df["fips"] = df["BENE_GEO_CD"].astype(str).str.extract(r"(\d+)")[0]
df["fips"] = df["fips"].str.zfill(5)

df = df[df["fips"].notna()]
df = df[~df["fips"].isin(["00000", "10000", "01000", "99999"])]

print("After FIPS cleaning:", df.shape)

# ----------------------------
# STEP 3: CLEAN NUMERIC COLUMNS
# ----------------------------
for col in df.columns:
    if col not in ["BENE_GEO_LVL", "BENE_GEO_DESC", "BENE_GEO_CD", "fips"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

# ----------------------------
# STEP 4: CREATE PQI INDEX (IMPORTANT FIX - BEFORE AGGREGATION)
# ----------------------------
pqi_cols = [c for c in df.columns if "PQI" in c]

if len(pqi_cols) > 0:
    df["preventable_burden_index"] = df[pqi_cols].mean(axis=1, skipna=True)
else:
    df["preventable_burden_index"] = 0

# ----------------------------
# STEP 5: AGGREGATE TO COUNTY-YEAR
# ----------------------------
df_clean = df.groupby(["fips", "YEAR"], as_index=False).mean(numeric_only=True)

print("After aggregation:", df_clean.shape)

# ----------------------------
# STEP 6: FEATURE SELECTION
# ----------------------------
keep_enrollment = [
    "BENES_TOTAL_CNT",
    "BENES_MA_CNT",
    "MA_PRTCPTN_RATE"
]

keep_utilization = [
    "BENES_IP_CVRD_STAY_CNT",
    "BENES_ER_VISITS_CNT",
    "BENES_OP_CNT",
    "BENES_SNF_CNT",
    "BENES_HH_CNT",
    "BENES_AMBLNC_CNT"
]

keep_enrollment = [c for c in keep_enrollment if c in df_clean.columns]
keep_utilization = [c for c in keep_utilization if c in df_clean.columns]

# ----------------------------
# STEP 7: FINAL STRUCTURE
# ----------------------------
df_clean = df_clean[
    ["fips", "YEAR"] +
    keep_enrollment +
    keep_utilization +
    ["preventable_burden_index"]
]

df_clean = df_clean.round(2)

# ----------------------------
# STEP 8: QUALITY CHECKS
# ----------------------------
print("\nFinal shape:", df_clean.shape)
print("Unique FIPS:", df_clean["fips"].nunique())
print(df_clean.head())

# ----------------------------
# STEP 9: SAVE
# ----------------------------
df_clean.to_csv(clean_path, index=False)

print("\nSaved to:", clean_path)
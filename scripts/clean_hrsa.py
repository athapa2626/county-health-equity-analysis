from pathlib import Path
import pandas as pd

# PATHS
project_root = Path(__file__).resolve().parents[1]

raw_path = project_root / "data" / "raw" / "hrsa_raw.csv"
clean_path = project_root / "data" / "clean" / "hrsa_clean.csv"

clean_path.parent.mkdir(parents=True, exist_ok=True)

# LOAD
df = pd.read_csv(raw_path, low_memory=False)

print("Raw shape:", df.shape)
print("Columns:", df.columns.tolist())

# STEP 1: FIND CORRECT FIPS COLUMN AUTOMATICALLY
fips_candidates = [c for c in df.columns if "FIPS" in c]

print("FIPS candidates:", fips_candidates)

if len(fips_candidates) == 0:
    raise ValueError("No FIPS column found in dataset")

fips_col = fips_candidates[0]   # take first valid match

df["fips"] = df[fips_col].astype(str).str.extract(r"(\d{5})")[0]

df = df[df["fips"].notna()]

print("After FIPS extraction:", df.shape)

# STEP 2: CLEAN CORE NUMERIC COLUMNS (SAFE CHECK)
numeric_cols = ["HPSA Score"]

for c in numeric_cols:
    if c in df.columns:
        df[c] = pd.to_numeric(df[c], errors="coerce")

# STEP 3: AGGREGATE (SAFE)
agg_dict = {}

if "HPSA Score" in df.columns:
    agg_dict["HPSA Score"] = "mean"

df_clean = df.groupby("fips", as_index=False).agg(agg_dict)

print("After aggregation:", df_clean.shape)

# STEP 4: FEATURES

# Standardize column name
df_clean = df_clean.rename(columns={
    "HPSA Score": "hpsa_score"
})

# Normalized score
if "hpsa_score" in df_clean.columns and df_clean["hpsa_score"].max() > 0:
    df_clean["hpsa_score_norm"] = (
        df_clean["hpsa_score"] / df_clean["hpsa_score"].max()
    )
else:
    df_clean["hpsa_score_norm"] = 0

# Binary shortage flag
df_clean["shortage_flag"] = (
    df_clean["hpsa_score"] >= 15
).astype(int)

# Round numeric columns
df_clean = df_clean.round(2)

# Reorder columns
df_clean = df_clean[
    [
        "fips",
        "hpsa_score",
        "hpsa_score_norm",
        "shortage_flag",
    ]
]

# SAVE
df_clean.to_csv(clean_path, index=False)

print("\nSaved:", clean_path)
print(df_clean.head())
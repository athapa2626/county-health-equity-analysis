from pathlib import Path
import pandas as pd

# Paths
project_root = Path(__file__).resolve().parents[1]

raw_path = project_root / "data" / "raw" / "acs_raw.csv"
clean_path = project_root / "data" / "clean" / "acs_clean.csv"

clean_path.parent.mkdir(parents=True, exist_ok=True)

# Load raw ACS data
df = pd.read_csv(
    raw_path,
    dtype={"state": str, "county": str},
    low_memory=False
)

print("Raw shape:", df.shape)

# Rename columns for clarity
df = df.rename(columns={
    "B01003_001E": "population",
    "B19013_001E": "median_income",
    "B17001_001E": "poverty_universe",
    "B17001_002E": "poverty_count",
    "NAME": "county_name"
})

# Create FIPS (state + county)
df["state"] = df["state"].str.zfill(2)
df["county"] = df["county"].str.zfill(3)
df["fips"] = df["state"] + df["county"]

# Convert numeric columns
numeric_cols = [
    "population",
    "median_income",
    "poverty_universe",
    "poverty_count"
]

for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Feature engineering

# Poverty rate (%)
df["poverty_rate"] = (
    df["poverty_count"] / df["poverty_universe"]
) * 100

# Optional: income per capita proxy check (kept simple)
df["income_per_capita_proxy"] = df["median_income"]

# Keep only relevant columns
df_clean = df[[
    "fips",
    "county_name",
    "population",
    "median_income",
    "poverty_count",
    "poverty_universe",
    "poverty_rate"
]]

# Round for readability
df_clean = df_clean.round(2)

# QA checks
print("\nFinal shape:", df_clean.shape)
print("\nMissing values:\n", df_clean.isnull().sum())
print("\nFIPS length check:", df_clean["fips"].str.len().value_counts())

# Ensure uniqueness (important for join keys)
print("\nUnique counties:", df_clean["fips"].nunique())

# Save cleaned dataset
df_clean.to_csv(clean_path, index=False)

print("\nACS cleaned dataset saved to:", clean_path)
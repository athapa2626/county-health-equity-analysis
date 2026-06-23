from pathlib import Path
import pandas as pd

# Paths
project_root = Path(__file__).resolve().parents[1]

raw_path = project_root / "data" / "raw" / "cdc_raw.csv"
clean_path = project_root / "data" / "clean" / "cdc_clean.csv"

clean_path.parent.mkdir(parents=True, exist_ok=True)

# Load raw data (FIXED)
df = pd.read_csv(
    raw_path,
    dtype={"LocationID": str},   # IMPORTANT: preserve FIPS formatting
    low_memory=False
)

print("Raw shape:", df.shape)

# Keep only needed columns
df = df[[
    "LocationID",
    "Measure",
    "Data_Value"
]]

df.columns = ["fips", "measure", "value"]

# Ensure proper FIPS format (5 digits)
df["fips"] = df["fips"].str.zfill(5)

# Keep only selected measures
selected_measures = {
    "Diagnosed diabetes among adults": "diabetes",
    "Obesity among adults": "obesity",
    "Current smoking among adults": "smoking",
    "Mental health not good for >=14 days among adults": "mental_health",
    "No leisure-time physical activity among adults": "inactivity"
}

df = df[df["measure"].isin(selected_measures.keys())]

df["measure"] = df["measure"].map(selected_measures)

# Convert to numeric
df["value"] = pd.to_numeric(df["value"], errors="coerce")

# Pivot long → wide
df_wide = df.pivot_table(
    index="fips",
    columns="measure",
    values="value",
    aggfunc="mean"
).reset_index()

df_wide.columns.name = None

# Round values (IMPORTANT for readability)
df_wide = df_wide.round(2)

# QA checks
print("\nFinal shape:", df_wide.shape)
print("\nMissing values:\n", df_wide.isnull().sum())
print("\nFIPS length check:", df_wide["fips"].str.len().value_counts())

# Save cleaned dataset
df_wide.to_csv(clean_path, index=False)

print("\nCDC cleaned dataset saved to:", clean_path)
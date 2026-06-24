from pathlib import Path
import pandas as pd

# PATHS
project_root = Path(__file__).resolve().parents[1]

clean_dir = project_root / "data" / "clean"
final_dir = project_root / "data" / "final"

final_dir.mkdir(parents=True, exist_ok=True)

# LOAD CLEAN DATASETS
acs = pd.read_csv(clean_dir / "acs_clean.csv", dtype={"fips": str})
cdc = pd.read_csv(clean_dir / "cdc_clean.csv", dtype={"fips": str})
cms = pd.read_csv(clean_dir / "cms_clean.csv", dtype={"fips": str})
hrsa = pd.read_csv(clean_dir / "hrsa_clean.csv", dtype={"fips": str})

print("Loaded datasets")
print(f"ACS : {acs.shape}")
print(f"CDC : {cdc.shape}")
print(f"CMS : {cms.shape}")
print(f"HRSA: {hrsa.shape}")

# --------------------------------------------------
# CLEAN COLUMN NAMES (SAFETY STEP)
# --------------------------------------------------
cms.columns = cms.columns.str.lower()
hrsa.columns = hrsa.columns.str.lower()
cdc.columns = cdc.columns.str.lower()
acs.columns = acs.columns.str.lower()

# --------------------------------------------------
# KEEP MOST RECENT CMS YEAR
# --------------------------------------------------
if "year" in cms.columns:
    latest_year = cms["year"].max()
    cms = cms[cms["year"] == latest_year].copy()
    cms = cms.drop(columns=["year"])
else:
    raise ValueError("CMS dataset missing 'year' column")

print(f"\nUsing CMS year: {latest_year}")
print(f"CMS rows after filtering: {cms.shape[0]}")

# --------------------------------------------------
# MERGE DATASETS
# --------------------------------------------------
master = (
    acs
    .merge(cdc, on="fips", how="left")
    .merge(hrsa, on="fips", how="left")
    .merge(cms, on="fips", how="left")
)

# --------------------------------------------------
# DROP UNUSED / LEGACY COLUMNS SAFELY
# --------------------------------------------------
cols_to_drop = [
    "preventable_burden_index"  # may or may not exist depending on CMS cleaning
]

master = master.drop(columns=[c for c in cols_to_drop if c in master.columns])

# --------------------------------------------------
# TYPE FIXES
# --------------------------------------------------
# FORMAT DATA TYPES
if "shortage_flag" in master.columns:
    master["shortage_flag"] = master["shortage_flag"].astype("float")

    # Convert missing HRSA data to -1 (Unknown)
    master["shortage_flag"] = master["shortage_flag"].fillna(-1)

    # Convert to integer after filling
    master["shortage_flag"] = master["shortage_flag"].astype("int64")

# Ensure FIPS formatting consistency
master["fips"] = master["fips"].astype(str).str.zfill(5)

# --------------------------------------------------
# ROUND NUMERIC COLUMNS
# --------------------------------------------------
numeric_cols = master.select_dtypes(include="number").columns
master[numeric_cols] = master[numeric_cols].round(2)

# --------------------------------------------------
# SORT + VALIDATION
# --------------------------------------------------
master = master.sort_values("fips").reset_index(drop=True)

assert master["fips"].is_unique, "Duplicate FIPS found!"
assert master["fips"].str.len().eq(5).all(), "Invalid FIPS length!"

# --------------------------------------------------
# SUMMARY
# --------------------------------------------------
print("\n----------------------------")
print("MASTER DATASET SUMMARY")
print("----------------------------")

print(f"Rows: {master.shape[0]}")
print(f"Columns: {master.shape[1]}")

print("\nDuplicate FIPS:")
print(master["fips"].duplicated().sum())

print("\nMissing Values (top 15):")
print(master.isna().sum().sort_values(ascending=False).head(15))

print("\nPreview:")
print(master.head())

# --------------------------------------------------
# SAVE FINAL DATASET
# --------------------------------------------------
output_path = final_dir / "master_health_dataset.csv"
master.to_csv(output_path, index=False)

print(f"\nMaster dataset saved to:\n{output_path}")
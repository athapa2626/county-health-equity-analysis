from pathlib import Path
import sqlite3
import pandas as pd

# --------------------------------------------------
# Paths
# --------------------------------------------------

project_root = Path(__file__).resolve().parents[1]

csv_path = project_root / "data" / "final" / "master_health_dataset.csv"
db_path = project_root / "database" / "county_health.db"
views_path = project_root / "sql" / "views.sql"

db_path.parent.mkdir(parents=True, exist_ok=True)

# --------------------------------------------------
# Load dataset
# --------------------------------------------------

df = pd.read_csv(csv_path, dtype={"fips": str})

print("Loaded dataset:")
print(df.shape)

# --------------------------------------------------
# Standardize column names
# --------------------------------------------------

df.columns = (
    df.columns
      .str.strip()
      .str.lower()
      .str.replace(" ", "_")
)

# --------------------------------------------------
# Remove duplicate counties
# --------------------------------------------------

before = len(df)
df = df.drop_duplicates(subset="fips")
after = len(df)

print(f"\nDuplicates removed: {before-after}")

# --------------------------------------------------
# Create database
# --------------------------------------------------

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Replace existing table
df.to_sql(
    "county_health",
    conn,
    if_exists="replace",
    index=False
)

# --------------------------------------------------
# Create index
# --------------------------------------------------

cursor.execute("""
CREATE INDEX IF NOT EXISTS idx_fips
ON county_health(fips);
""")

# --------------------------------------------------
# Execute SQL Views (SAFE RE-RUN - FULL RESET)
# --------------------------------------------------

if views_path.exists():
    with open(views_path, "r", encoding="utf-8") as f:
        view_sql = f.read()

    # STEP 1: Drop ALL existing views dynamically
    existing_views = pd.read_sql(
        "SELECT name FROM sqlite_master WHERE type='view';",
        conn
    )["name"].tolist()

    drop_statements = "\n".join(
        [f"DROP VIEW IF EXISTS {v};" for v in existing_views]
    )

    cursor.executescript(drop_statements)

    # STEP 2: Recreate views
    cursor.executescript(view_sql)

    print("\nSQL views recreated successfully.")
else:
    print("\nNo views.sql found. Skipping view creation.")

conn.commit()

# --------------------------------------------------
# QA Checks
# --------------------------------------------------

rows = pd.read_sql(
    "SELECT COUNT(*) AS rows FROM county_health",
    conn
)

print("\nRows imported:")
print(rows)

preview = pd.read_sql(
    "SELECT * FROM county_health LIMIT 5",
    conn
)

print("\nPreview:")
print(preview)

# Show views
views = pd.read_sql("""
SELECT name
FROM sqlite_master
WHERE type='view'
ORDER BY name;
""", conn)

if len(views):
    print("\nViews:")
    print(views)
else:
    print("\nNo SQL views found.")

conn.close()

print("\nDatabase successfully created at:")
print(db_path)
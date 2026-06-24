from pathlib import Path
import sqlite3
import pandas as pd

# --------------------------------------------------
# PATHS
# --------------------------------------------------

project_root = Path(__file__).resolve().parents[1]

db_path = project_root / "database" / "county_health.db"
sql_path = project_root / "sql" / "queries.sql"
output_dir = project_root / "outputs"

output_dir.mkdir(exist_ok=True)

# CONNECT TO DATABASE
conn = sqlite3.connect(db_path)

# LOAD QUERIES
with open(sql_path, "r") as f:
    queries = f.read().split(";")

# EXECUTE QUERIES
for i, query in enumerate(queries):
    query = query.strip()

    if not query:
        continue

    print("\n" + "=" * 60)
    print(f"QUERY {i + 1}")
    print("=" * 60)

    try:
        df = pd.read_sql_query(query, conn)

        # show preview
        print(df.head(10))
        print(f"\nRows returned: {len(df)}")

        # SAVE OUTPUT
        output_path = output_dir / f"query_{i + 1}.csv"
        df.to_csv(output_path, index=False)

    except Exception as e:
        print(f"Error running query {i + 1}: {e}")

# CLEAN UP
conn.close()

print("\nAll queries executed successfully.")
print(f"Outputs saved to: {output_dir}")
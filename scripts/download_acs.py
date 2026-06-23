from pathlib import Path
import requests
import pandas as pd
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

API_KEY = os.getenv("CENSUS_API_KEY")

if API_KEY is None:
    raise ValueError("CENSUS_API_KEY not found in .env file")

# Create output folder if needed
project_root = Path(__file__).resolve().parents[1]
output_dir = project_root / "data" / "raw"
output_dir.mkdir(parents=True, exist_ok=True)

output_file = output_dir / "acs_raw.csv"

# ACS 5-Year API endpoint
url = "https://api.census.gov/data/2023/acs/acs5"

# Variables we'll download
variables = [
    "NAME",          # County name
    "B01003_001E",   # Total population
    "B19013_001E",   # Median household income
    "B17001_001E",   # Poverty universe
    "B17001_002E"    # Population below poverty
]

params = {
    "get": ",".join(variables),
    "for": "county:*",
    "key": API_KEY
}

print("Requesting ACS data...")

response = requests.get(url, params=params)
response.raise_for_status()

data = response.json()

# Convert to DataFrame
df = pd.DataFrame(data[1:], columns=data[0])

# Save raw CSV
df.to_csv(output_file, index=False)

print(f"ACS data saved to:\n{output_file}")
print(f"Rows: {len(df)}")
print(f"Columns: {len(df.columns)}")
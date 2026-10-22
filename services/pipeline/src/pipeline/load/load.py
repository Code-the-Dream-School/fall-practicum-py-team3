import os
from datetime import datetime, timezone
from pathlib import Path
from dotenv import dotenv_values
from supabase import create_client
from pipeline.extract.extract import extract as ext, City

# Find the directory containing setup_env.py
# Navigate to the project root
project_root = Path(__file__).resolve().parents[5]

# Construct the full path to .env
env_path = project_root / ".env"

# Read configuration
config = dotenv_values(env_path)

supabase_url = config.get("SUPABASE_URL")
supabase_key = config.get("SUPABASE_KEY")

if not supabase_url:
    raise ValueError(f"Url is not in {env_path}.")

if not supabase_key:
    raise ValueError(f"Key is not in {env_path}.")

supabase = create_client(supabase_url, supabase_key)

# Flatten data
def flatten_raw(data):
    retrieved_at = datetime.now(timezone.utc)
    print(retrieved_at.isoformat())
    flatten_air_data = []
    
    for aqi in data["list"]:
        air_props = aqi["components"]
        
        record = {
            # city variable from above
            "timestamp": datetime.fromtimestamp(
                air_props["time"] / 1000,
                tz=timezone.utc
            ).isoformat(),
            # aqi & main
            # add each pollutant
            # retrieved_at
        }
        flatten_air_data.append(record)
    return flatten_air_data

# Load raw data to db
def load_raw(ext):
    response = (
        supabase.table("raw_air_quality")
        .upsert(ext, on_conflict="city, timestamp")
        .execute()
    )

    print(f"Upserted {len(response.data)} rows into raw_air_quality")
 
# Attempt 1   
# flattened = flatten_raw(City)
# load_raw(flattened)

# Attempt 2
# extraction = ext(City)
# load_raw(extraction)
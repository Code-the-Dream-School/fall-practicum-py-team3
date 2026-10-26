import os
from pathlib import Path
from dotenv import dotenv_values
from supabase import create_client
import data_contracts.schemas as schemas
from pipeline.extract.extract import extract as ext, City

# Find the directory containing setup_env.py
# Navigate to the project root
project_root = Path(__file__).resolve().parents[5]

# Construct the full path to .env
env_path = project_root / ".env"

# Read configuration
config = dotenv_values(env_path)
ext.__globals__["API_KEY"] = config.get("OPENWEATHER_API_KEY")

supabase_url = config.get("SUPABASE_URL")
supabase_key = config.get("SUPABASE_KEY")

if not supabase_url:
    raise ValueError(f"Url is not in {env_path}.")

if not supabase_key:
    raise ValueError(f"Key is not in {env_path}.")

supabase = create_client(supabase_url, supabase_key)

# Load raw data to db
def load_raw(ext):
    try:
        
        response = (
            supabase.table("raw_air_quality")
            .upsert(ext, on_conflict="city,timestamp")
            .execute()
        )

        print(f"Upserted {len(response.data)} rows into raw_air_quality")
    
    except Exception as error:
        print(f"Failed to load raw air quality records: {error}.")
        raise
 
if __name__ == "__main__":
    city = City(
    LAT=35.2271,
    LON=-80.8431,
    START=1761350400, 
    END=1792886400
    )

    extraction = ext(city)
    records = extraction.to_raw_schema("Charlotte")
    print("Records:", len(records))
    load_raw(records)
import os
from pathlib import Path
from dotenv import dotenv_values
from supabase import create_client
import data_contracts.schemas as schemas
from pipeline.extract.extract import extract as ext, City, CITIES
from pipeline.run_tracking import start_run, finish_run, fail_run

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
        # Records are unique by city and timestamp.
        # Upsert updates existing records instead of creating duplicates.
        response = (
            supabase.table("raw_air_quality")
            .upsert(ext, on_conflict="city,timestamp")
            .select()
            .execute()
        )

        print(f"Upserted {len(response.data)} rows into raw_air_quality")
        return len(response.data)
    
    except Exception as error:
        print(f"Failed to load raw air quality records: {error}.")
        raise

def main():
    run_id = start_run()
    rows_loaded = 0
    
    try:
        for name, coords in CITIES.items():
            city = City(
                LAT=coords["LAT"],
                LON=coords["LON"],
                START=1761350400, 
                END=1792886400
            )

            extraction = ext(city)
            records = extraction.to_raw_schema(name)
            
            print(f"{name} records: {len(records)}")
            
            rows_loaded += load_raw(records)
            
        finish_run(
            run_id,
            rows_extracted=0,
            rows_transformed=0,
            rows_loaded=rows_loaded,
        )
        
        print("Raw loading completed successfully.")
        
    except Exception as error:
        fail_run(
            run_id,
            error,
            rows_loaded=rows_loaded,
        )
        raise
    
if __name__ == "__main__":
    main()
import os
from pathlib import Path
from dotenv import dotenv_values
from sqlalchemy.dialects.postgresql import insert
import data_contracts.schemas as schemas
from pipeline.db import engine, table
from pipeline.extract.extract import extract as ext, City, CITIES

# Find the directory containing setup_env.py
# Navigate to the project root
project_root = Path(__file__).resolve().parents[5]

# Construct the full path to .env
env_path = project_root / ".env"

# Read configuration
config = dotenv_values(env_path)
ext.__globals__["API_KEY"] = config.get("OPENWEATHER_API_KEY")

# Load raw data to db
def load_raw(ext):
    try:
        raw = table("raw_air_quality")

        # Records are unique by city and timestamp.
        # Upsert updates existing records instead of creating duplicates.
        upsert = insert(raw)
        upsert = upsert.on_conflict_do_update(
            index_elements=["city", "timestamp"],
            set_={c.name: upsert.excluded[c.name] for c in raw.c if not c.primary_key},
        )
        with engine().begin() as conn:
            conn.execute(upsert, ext)

        print(f"Upserted {len(ext)} rows into raw_air_quality")
    
    except Exception as error:
        print(f"Failed to load raw air quality records: {error}.")
        raise

if __name__ == "__main__":
    
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
        load_raw(records)
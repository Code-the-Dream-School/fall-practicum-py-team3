from pathlib import Path
from supabase import create_client
import data_contracts.schemas as schemas
from pipeline.config import settings
from pipeline.extract.extract import extract as ext, City, CITIES

supabase = (
    create_client(settings.supabase_url, settings.supabase_key)
    if settings.supabase_url and settings.supabase_key
    else None
)

# Load raw data to db
def load_raw(ext):
    if supabase is None:
        raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set. Check .env.")
    try:
        # Records are unique by city and timestamp.
        # Upsert updates existing records instead of creating duplicates.
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
import os
from pathlib import Path
from dotenv import dotenv_values
from supabase import create_client
from pipeline.extract.extract import extract as ext

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

def load_raw(ext):
    response = (
        supabase.table("raw_air_quality")
        .upsert(ext, on_conflict="city, timestamp")
        .execute()
    )

    print(f"Upserted {len(response.data)} rows into raw_air_quality")
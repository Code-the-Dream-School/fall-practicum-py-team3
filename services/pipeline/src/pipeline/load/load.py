import os
from pathlib import Path
from dotenv import dotenv_values
from supabase import create_client
import pipeline.extract.extract as ext

# Find the directory containing setup_env.py
current_dir = Path(__file__).resolve().parent

# Navigate to the project root
project_root = current_dir.parent.parent

# Construct the full path to .env
env_path = project_root / ".env"

# Read configuration
config = dotenv_values(env_path)

supabase_url = config.get("SUPABASE_URL")
supabase_key = config.get("SUPABASE_KEY")

if not supabase_url:
    raise ValueError(f"{supabase_url} is not in {env_path}.")

if not supabase_key:
    raise ValueError(f"{supabase_key} is not in {env_path}.")

supabase = create_client(supabase_url, supabase_key)

def load_raw(ext):
    response = (
        supabase.table("raw_air_quality")
        .upsert(ext, on_confilct="city, timestamp")
        .execute()
    )

    print(f"Upserted {len(response.data)} rows into raw_air_quality")
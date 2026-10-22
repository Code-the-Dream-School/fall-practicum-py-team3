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
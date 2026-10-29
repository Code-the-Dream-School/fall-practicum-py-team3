import os
from functools import cache

from dotenv import load_dotenv
from sqlalchemy import MetaData, Table, create_engine

load_dotenv()

_metadata = MetaData(schema="city_air")


@cache
def engine():
    url = os.environ.get("SUPABASE_DB_URL")
    if not url:
        raise RuntimeError("SUPABASE_DB_URL must be set. Check .env.")
    return create_engine(url, pool_pre_ping=True)


@cache
def table(name):
    """A city_air table with its columns read from the database (migrations define them)."""
    return Table(name, _metadata, autoload_with=engine())

"""Shared Supabase client creation."""

from supabase import create_client

from pipeline.config import settings

_client = None


def get_supabase_client():
    global _client
    if _client is None:
        if not settings.supabase_url or not settings.supabase_key:
            raise RuntimeError("SUPABASE_URL and SUPABASE_KEY must be set. Check .env.")
        _client = create_client(settings.supabase_url, settings.supabase_key)
    return _client



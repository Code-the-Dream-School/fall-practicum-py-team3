import os
from datetime import datetime, timezone

from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

_client = None


def _connect():
    global _client
    if _client is None:
        url = os.environ.get("SUPABASE_URL")
        key = os.environ.get("SUPABASE_KEY")
        if not url or not key:
            raise RuntimeError("SUPABASE_URL and SUPABASE_KEY must be set. Check .env.")
        _client = create_client(url, key)
    return _client


def _now():
    return datetime.now(timezone.utc).isoformat()


def start_run():
    """Open a run record. Returns the run_id the database assigned."""
    response = (
        _connect()
        .table("pipeline_runs")
        .insert({"status": "running", "started_at": _now()})
        .execute()
    )
    return response.data[0]["run_id"]


def finish_run(run_id, rows_extracted=None, rows_loaded=None, rows_transformed=None):
    _close(run_id, "success", rows_extracted, rows_loaded, rows_transformed, None)


def fail_run(run_id, error, rows_extracted=None, rows_loaded=None, rows_transformed=None):
    _close(run_id, "failed", rows_extracted, rows_loaded, rows_transformed, str(error))


def _close(run_id, status, rows_extracted, rows_loaded, rows_transformed, error_message):
    response = (
        _connect()
        .table("pipeline_runs")
        .update(
            {
                "status": status,
                "ended_at": _now(),
                "rows_extracted": rows_extracted,
                "rows_loaded": rows_loaded,
                "rows_transformed": rows_transformed,
                "error_message": error_message,
            }
        )
        .eq("run_id", run_id)
        .execute()
    )
    if not response.data:
        raise RuntimeError(f"No pipeline_runs row with run_id {run_id}")
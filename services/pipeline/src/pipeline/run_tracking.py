from datetime import datetime, timezone

from pipeline.db import get_supabase_client


def _now():
    return datetime.now(timezone.utc).isoformat()


def start_run(run_mode=None, window_start=None, window_end=None):
    """Open a run record. Returns the run_id the database assigned."""
    response = (
        get_supabase_client()
        .table("pipeline_runs")
        .insert({"status": "running", "started_at": _now(), "run_mode": run_mode, "window_start": window_start, "window_end": window_end})
        .execute()
    )
    return response.data[0]["run_id"]

# get most recent successful backfill or incremental run
def get_last_successful_run():
    response = (
        get_supabase_client()
        .table("pipeline_runs")
        .select("run_id, run_mode, window_start, window_end, ended_at")
        .eq("status", "success")
        .in_("run_mode", ["backfill", "incremental"])
        .not_.is_("window_end", "null")
        .order("ended_at", desc=True)
        .limit(1)
        .execute()
    )
    
    return response.data[0] if response.data else None


def finish_run(run_id, rows_extracted=None, rows_loaded=None, rows_transformed=None):
    _close(run_id, "success", rows_extracted, rows_loaded, rows_transformed, None)


def fail_run(run_id, error, rows_extracted=None, rows_loaded=None, rows_transformed=None):
    _close(run_id, "failed", rows_extracted, rows_loaded, rows_transformed, str(error))


def _close(run_id, status, rows_extracted, rows_loaded, rows_transformed, error_message):
    response = (
        get_supabase_client()
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
import os
import psycopg
from dotenv import load_dotenv

load_dotenv("dev.env")


def _connect():
    dsn = os.environ.get("DATABASE_URL")
    if not dsn:
        raise RuntimeError("DATABASE_URL is not set. Check .env.")
    return psycopg.connect(dsn)


def start_run():
    """Open a run record. Returns the run_id the database assigned."""
    with _connect() as conn, conn.cursor() as cur:
        cur.execute(
            "INSERT INTO pipeline_runs (status, started_at) "
            "VALUES ('running', now()) RETURNING run_id"
        )
        return cur.fetchone()[0]

def finish_run(run_id, rows_extracted=None, rows_loaded=None, rows_transformed=None):
    _close(run_id, "success", rows_extracted, rows_loaded, rows_transformed, None)
    
def fail_run(run_id, error, rows_extracted=None, rows_loaded=None, rows_transformed=None):
    _close(run_id, "failed", rows_extracted, rows_loaded, rows_transformed, str(error))

def _close(run_id, status, rows_extracted, rows_loaded, rows_transformed, error_message):
    with _connect() as conn, conn.cursor() as cur:
        cur.execute(
            """
            UPDATE pipeline_runs
            SET status           = %s,
                ended_at         = now(),
                rows_extracted   = %s,
                rows_loaded      = %s,
                rows_transformed = %s,
                error_message    = %s
            WHERE run_id = %s
            """,
            (status, rows_extracted, rows_loaded, rows_transformed, error_message, run_id),
        )
        if cur.rowcount == 0:
            raise RuntimeError(f"No pipeline_runs row with run_id {run_id}")
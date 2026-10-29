from sqlalchemy import func, insert, update

from pipeline.db import engine, table


def start_run():
    """Open a run record. Returns the run_id the database assigned."""
    runs = table("pipeline_runs")
    with engine().begin() as conn:
        return conn.execute(
            insert(runs)
            .values(status="running", started_at=func.now())
            .returning(runs.c.run_id)
        ).scalar_one()


def finish_run(run_id, rows_extracted=None, rows_loaded=None, rows_transformed=None):
    _close(run_id, "success", rows_extracted, rows_loaded, rows_transformed, None)


def fail_run(run_id, error, rows_extracted=None, rows_loaded=None, rows_transformed=None):
    _close(run_id, "failed", rows_extracted, rows_loaded, rows_transformed, str(error))


def _close(run_id, status, rows_extracted, rows_loaded, rows_transformed, error_message):
    runs = table("pipeline_runs")
    with engine().begin() as conn:
        result = conn.execute(
            update(runs)
            .where(runs.c.run_id == run_id)
            .values(
                status=status,
                ended_at=func.now(),
                rows_extracted=rows_extracted,
                rows_loaded=rows_loaded,
                rows_transformed=rows_transformed,
                error_message=error_message,
            )
        )
    if result.rowcount == 0:
        raise RuntimeError(f"No pipeline_runs row with run_id {run_id}")

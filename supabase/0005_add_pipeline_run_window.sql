-- UP
ALTER TABLE pipeline_runs
ADD COLUMN IF NOT EXISTS run_mode TEXT,
ADD COLUMN IF NOT EXISTS window_start TIMESTAMPTZ,
ADD COLUMN IF NOT EXISTS window_end TIMESTAMPTZ;

ALTER TABLE pipeline_runs
ADD CONSTRAINT pipeline_runs_run_mode_check
    CHECK (run_mode IN ('backfill','incremental'));

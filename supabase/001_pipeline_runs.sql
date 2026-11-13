CREATE TABLE IF NOT EXISTS pipeline_runs (
    run_id           BIGINT       GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    created_at       TIMESTAMPTZ  NOT NULL DEFAULT now(),
    started_at       TIMESTAMPTZ, 
    ended_at         TIMESTAMPTZ,
    status           TEXT         NOT NULL DEFAULT 'pending',
    rows_extracted   INTEGER,     
    rows_transformed INTEGER,     
    rows_loaded      INTEGER,     
    error_message    TEXT,
    run_mode         TEXT,
    window_start     TIMESTAMPTZ,
    window_end       TIMESTAMPTZ,

    CONSTRAINT pipeline_runs_status_check
        CHECK (status IN ('pending','running', 'success', 'failed'))

    CONSTRAINT pipeline_runs_run_mode_check
        CHECK (run_mode IN ('backfill','incremental'))

);

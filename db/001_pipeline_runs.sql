
CREATE TABLE IF NOT EXISTS pipeline_runs (
    pipeline_run_id  BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    run_id           TEXT        NOT NULL UNIQUE,
    status           TEXT        NOT NULL DEFAULT 'running',
    started_at       TIMESTAMPTZ NOT NULL DEFAULT now(),
    finished_at      TIMESTAMPTZ,
    rows_extracted   INTEGER,
    rows_loaded      INTEGER,
    rows_transformed INTEGER,
    error_message    TEXT,

    CONSTRAINT pipeline_runs_status_check
        CHECK (status IN ('running', 'succeeded', 'failed'))
);
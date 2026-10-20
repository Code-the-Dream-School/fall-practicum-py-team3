CREATE TABLE IF NOT EXISTS pipeline_runs (
    run_id           BIGINT      GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    started_at       TIMESTAMPTZ NOT NULL DEFAULT now(),
    ended_at         TIMESTAMPTZ,
    status           TEXT        NOT NULL DEFAULT 'running',
    rows_extracted   INTEGER     NOT NULL DEFAULT 0,
    rows_transformed INTEGER     NOT NULL DEFAULT 0,
    rows_loaded      INTEGER     NOT NULL DEFAULT 0,
    error_message    TEXT,

    CONSTRAINT pipeline_runs_status_check
        CHECK (status IN ('running', 'success', 'failed'))
);
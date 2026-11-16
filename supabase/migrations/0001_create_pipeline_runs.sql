-- Migration: 0001_create_pipeline_runs
-- Purpose: track pipeline run lifecycle and row counts.

-- up
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
    CONSTRAINT pipeline_runs_status_check
        CHECK (status IN ('pending', 'running', 'success', 'failed'))
);

-- down
DROP TABLE IF EXISTS pipeline_runs;
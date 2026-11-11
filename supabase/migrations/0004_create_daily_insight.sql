-- Migration: 0004_create_daily_insight
-- Purpose: LLM-enriched daily insight text per city/timestamp.

-- up
CREATE TABLE IF NOT EXISTS daily_insight (
    city              TEXT        NOT NULL,
    timestamp         TIMESTAMPTZ NOT NULL,
    date              DATE        NOT NULL,
    category          TEXT,
    aqi_24h_avg       NUMERIC,
    insight_text      TEXT,
    insight_source    TEXT,
    model             TEXT,
    prompt_version    TEXT,
    enriched_at       TIMESTAMPTZ,
    enrichment_error  TEXT,
    PRIMARY KEY (city, timestamp)
);

CREATE INDEX IF NOT EXISTS daily_insight_city_date_idx
    ON daily_insight (city, date);

-- down
DROP TABLE IF EXISTS daily_insight;
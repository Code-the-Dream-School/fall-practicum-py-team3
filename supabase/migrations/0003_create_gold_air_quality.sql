-- Migration: 0003_create_gold_air_quality
-- Purpose: transformed/gold air-quality records with derived metrics.

-- up
CREATE TABLE IF NOT EXISTS gold_air_quality (
    city          TEXT        NOT NULL,
    timestamp     TIMESTAMPTZ NOT NULL,
    aqi           NUMERIC,
    co            NUMERIC,
    no            NUMERIC,
    no2           NUMERIC,
    o3            NUMERIC,
    so2           NUMERIC,
    pm2_5         NUMERIC,
    pm10          NUMERIC,
    nh3           NUMERIC,
    category      TEXT,
    score         NUMERIC,
    aqi_24h_avg   NUMERIC     NOT NULL,
    PRIMARY KEY (city, timestamp)
);

CREATE INDEX IF NOT EXISTS gold_air_quality_city_timestamp_idx
    ON gold_air_quality (city, timestamp);

-- down
DROP TABLE IF EXISTS gold_air_quality;
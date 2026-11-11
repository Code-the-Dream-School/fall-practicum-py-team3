-- Migration: 0002_create_raw_air_quality
-- Purpose: store raw OpenWeather air-quality readings per city/timestamp.

-- up
CREATE TABLE IF NOT EXISTS raw_air_quality (
    city         TEXT             NOT NULL,
    timestamp    TIMESTAMPTZ      NOT NULL,
    aqi          DOUBLE PRECISION,
    co           DOUBLE PRECISION,
    no           DOUBLE PRECISION,
    no2          DOUBLE PRECISION,
    o3           DOUBLE PRECISION,
    so2          DOUBLE PRECISION,
    pm2_5        DOUBLE PRECISION,
    pm10         DOUBLE PRECISION,
    nh3          DOUBLE PRECISION,
    retrieved_at TIMESTAMPTZ      NOT NULL,
    PRIMARY KEY (city, timestamp)
);

ALTER TABLE raw_air_quality ENABLE ROW LEVEL SECURITY;

CREATE INDEX IF NOT EXISTS raw_air_quality_city_timestamp_idx
    ON raw_air_quality (city, timestamp);

-- down
DROP TABLE IF EXISTS raw_air_quality;
CREATE TABLE IF NOT EXISTS daily_insight (

  city TEXT NOT NULL,
  timestamp DATE NOT NULL,
  category TEXT, 
  aqi_24h_avg NUMERIC,
  insight_text TEXT,
  insight_source TEXT,
  enriched_at TIMESTAMPTZ,
  PRIMARY KEY (city, timestamp)
);

-- add enriched_at if table already existed
ALTER TABLE daily_insight
ADD COLUMN IF NOT EXISTS enriched_at TIMESTAMPTZ;

-- remove month if it exists
ALTER TABLE daily_insight
DROP COLUMN IF EXISTS month;

-- change timestamp to DATE if needed
ALTER TABLE daily_insight
ALTER COLUMN timestamp TYPE DATE USING timestamp::DATE;
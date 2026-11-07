CREATE TABLE IF NOT EXISTS daily_insight (

  city TEXT NOT NULL,
  timestamp TIMESTAMPTZ NOT NULL,
  date DATE NOT NULL,
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
ADD COLUMN IF NOT EXISTS timestamp TIMESTAMPTZ;

-- add date if it doesn't exist
ALTER TABLE daily_insight
ADD COLUMN IF NOT EXISTS date DATE;

-- ensure date is populated based on timestamp
UPDATE daily_insight
SET date = (timestamp AT TIME ZONE 'UTC')::DATE
WHERE date IS NULL;
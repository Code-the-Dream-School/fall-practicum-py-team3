CREATE TABLE IF NOT EXISTS daily_insight (

  city TEXT NOT NULL,
  timestamp TIMESTAMPTZ NOT NULL,
  month INTEGER,
  category TEXT, 
  aqi_24h_avg NUMERIC,
  insight_text TEXT,
  insight_source TEXT,
  enriched_at TIMESTAMPTZ,
  PRIMARY KEY (city, timestamp)
);


ALTER TABLE daily_insight
ADD COLUMN IF NOT EXISTS enriched_at TIMESTAMPTZ;
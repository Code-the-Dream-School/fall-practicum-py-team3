CREATE TABLE IF NOT EXISTS daily_insight (

  city TEXT NOT NULL,
  timestamp TIMESTAMPTZ NOT NULL,
  month INTEGER,
  category TEXT, 
  aqi_24h_avg NUMERIC,
  llm_summary TEXT,
  insight_source TEXT,
  PRIMARY KEY (city, timestamp)
);


-- ALTER TABLE daily_insight
-- ADD COLUMN 
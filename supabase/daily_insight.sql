CREATE TABLE IF NOT EXISTS daily_insight (

  city TEXT NOT NULL,
  timestamp TIMESTAMPTZ NOT NULL,
  date DATE NOT NULL,
  category TEXT, 
  aqi_24h_avg NUMERIC,
  insight_text TEXT,
  insight_source TEXT,
  model TEXT,
  prompt_version TEXT,
  enriched_at TIMESTAMPTZ,
  enrichment_error TEXT,
  PRIMARY KEY (city, timestamp)
);


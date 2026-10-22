CREATE TABLE IF NOT EXISTS raw_air_quality (
  city         TEXT             NOT NULL,
  timestamp    TIMESTAMPTZ      NOT NULL,  
  aqi          SMALLINT,                   
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

-- Only the service/secret key (pipeline) can access this table.
ALTER TABLE raw_air_quality ENABLE ROW LEVEL SECURITY;
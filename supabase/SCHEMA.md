# Supabase Schema

## Tables

### pipeline_runs
Tracks each pipeline execution.

| Column | Type | Notes |
|---|---|---|
| run_id | BIGINT (PK, identity) | |
| created_at | TIMESTAMPTZ | default now() |
| started_at / ended_at | TIMESTAMPTZ | |
| status | TEXT | pending/running/success/failed |
| rows_extracted / rows_transformed / rows_loaded | INTEGER | |
| error_message | TEXT | |

### raw_air_quality
Raw OpenWeather readings. PK `(city, timestamp)`.

| Column | Type | Notes |
|---|---|---|
| city | TEXT (PK) | |
| timestamp | TIMESTAMPTZ (PK) | |
| aqi | DOUBLE PRECISION | OpenWeather 1-5 |
| co, no, no2, o3, so2, pm2_5, pm10, nh3 | DOUBLE PRECISION | µg/m³ |
| retrieved_at | TIMESTAMPTZ | NOT NULL |

### gold_air_quality
Transformed records with derived `category`, `score`, `aqi_24h_avg`. PK `(city, timestamp)`.

| Column | Type | Notes |
|---|---|---|
| city | TEXT (PK) | |
| timestamp | TIMESTAMPTZ (PK) | |
| aqi | NUMERIC | OpenWeather 1-5 |
| co, no, no2, o3, so2, pm2_5, pm10, nh3 | NUMERIC | µg/m³ |
| category | TEXT | Good/Fair/... |
| score | NUMERIC | sub-index score |
| aqi_24h_avg | NUMERIC (NOT NULL) | rolling 24h avg |

### daily_insight
LLM-enriched daily insight text. PK `(city, timestamp)`.

| Column | Type | Notes |
|---|---|---|
| city | TEXT (PK) | |
| timestamp | TIMESTAMPTZ (PK) | |
| date | DATE (NOT NULL) | |
| category | TEXT | |
| aqi_24h_avg | NUMERIC | |
| insight_text | TEXT | generated insight |
| insight_source | TEXT | template/llm |
| model | TEXT | model name |
| prompt_version | TEXT | |
| enriched_at | TIMESTAMPTZ | |
| enrichment_error | TEXT | |

## Relationships
- `gold_air_quality` and `daily_insight` share PK `(city, timestamp)` with `raw_air_quality`.
- `pipeline_runs` is standalone (no FK to data tables).
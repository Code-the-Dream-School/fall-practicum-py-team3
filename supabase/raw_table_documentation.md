# Raw Air Quality Table

The `raw_air_quality` table stores unmodified hourly air-quality values from the
OpenWeather Air Pollution API, one row per city per hour. "Raw" means the values
are kept as the API returned them. They are not cleaned or filled in.

The table is `city_air.raw_air_quality`, created by the Alembic migrations in
`db/migrations/`. See [db/README.md](../db/README.md) for how to apply them.

## Keys and requirements

- **Primary key:** (city, timestamp). Identifies each record by its city and observation time.
- **Foreign keys:** None used.
- **Uniqueness:** Each city can have only one record per timestamp, enforced by the
  primary key. Reloading the same data should upsert on (city, timestamp), not duplicate it.
- **Required columns (NOT NULL):** city, timestamp, retrieved_at
- **Optional columns (nullable):** aqi, co, no, no2, o3, so2, pm2_5, pm10, nh3.
  Missing values from the API stay NULL. They are not replaced with 0 or an average.
- **Access:** the `city_air` schema is not reachable through the Supabase API; the
  pipeline connects to Postgres directly. Row Level Security is also enabled, with no policies.

## Mapping from the API response

| API field | Column | Type |
|---|---|---|
| (city from the city list) | city | TEXT |
| list[].dt | timestamp | TIMESTAMPTZ (UTC) |
| list[].main.aqi | aqi | DOUBLE PRECISION |
| list[].components.co | co | DOUBLE PRECISION |
| list[].components.no | no | DOUBLE PRECISION |
| list[].components.no2 | no2 | DOUBLE PRECISION |
| list[].components.o3 | o3 | DOUBLE PRECISION |
| list[].components.so2 | so2 | DOUBLE PRECISION |
| list[].components.pm2_5 | pm2_5 | DOUBLE PRECISION |
| list[].components.pm10 | pm10 | DOUBLE PRECISION |
| list[].components.nh3 | nh3 | DOUBLE PRECISION |
| time of the API call | retrieved_at | TIMESTAMPTZ (UTC) |

Not stored per row: the request latitude, longitude, start and end. They repeat on
every hourly row, and the city list config already holds the coordinates.

## Changing the schema

Don't edit tables by hand in the dashboard. Add a migration in a pull request
(see [db/README.md](../db/README.md)), so every database gets the same change.
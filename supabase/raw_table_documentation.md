# Raw Air Quality Table

The `raw_air_quality` table stores unmodified hourly air-quality values from the
OpenWeather Air Pollution API, one row per city per hour. "Raw" means the values
are kept as the API returned them. They are not cleaned or filled in.

The schema is defined in `supabase/raw_air_quality.sql`. Team members can use this
script to create the table in their own Supabase testing projects.

- Note: The script creates the table structure but does not insert data.

## Keys and requirements

- **Primary key:** (city, timestamp). Identifies each record by its city and observation time.
- **Foreign keys:** None used.
- **Uniqueness:** Each city can have only one record per timestamp, enforced by the
  primary key. Reloading the same data should upsert on (city, timestamp), not duplicate it.
- **Required columns (NOT NULL):** city, timestamp, retrieved_at
- **Optional columns (nullable):** aqi, co, no, no2, o3, so2, pm2_5, pm10, nh3.
  Missing values from the API stay NULL. They are not replaced with 0 or an average.
- **Row Level Security:** enabled with no policies, so only the secret key (backend)
  can read or write the table.

## Mapping from the API response

| API field | Column | Type |
|---|---|---|
| (city from the city list) | city | TEXT |
| list[].dt | timestamp | TIMESTAMPTZ (UTC) |
| list[].main.aqi | aqi | SMALLINT |
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

## How to run

1. Create your own Supabase project (or a local Postgres) for development.
2. In the Supabase dashboard, open **SQL Editor**, then **New query**.
3. Paste the contents of `supabase/raw_air_quality.sql` and click **Run**.
   - Or, with psql: `psql "<your connection string>" -f supabase/raw_air_quality.sql`
4. Open **Table Editor** and check that `raw_air_quality` exists with the columns above.
5. The script is safe to run again (`CREATE TABLE IF NOT EXISTS`).
6. To start from an empty database, run `raw_air_quality.sql` and `gold_air_quality.sql`.
   There are no foreign keys between them, so the order doesn't matter.

## Changing the schema

Don't edit tables by hand in the dashboard. Change the SQL file in a pull request,
so everyone applies the same version.
# Gold Air Quality Table

The gold_air_quality table stores cleaned and transformed hourly air-quality data for each city.

The table is `city_air.gold_air_quality`, created by the Alembic migrations in `db/migrations/`. See [db/README.md](../db/README.md) for how to apply them.

## Gold Table Keys and Requirements

- Primary key: (city, timestamp) - uniquely identifies each air-quality record by its city and observation time.
- Foreign keys: None used
- Uniqueness: Each city can only one record per timestamp which is enforced by the Primary key.
- Required columns: City and timestamp are NOT NULL.  We are including all Pollutants which can include missing data.  Also, Category and Score columns are required.  Possibly a daily.


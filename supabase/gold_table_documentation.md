# Gold Air Quality Table

The gold_air_quality table stores cleaned and transformed hourly air-quality data for each city.

The gold table schema is defined in supabase/gold_air_quality.sql. Team members can use this SQL script to create the Gold table in their own Supabase testing projects.

- Note: The script creates the table structure but does not insert data.

## Gold Table Keys and Requirements

- Primary key: (city, timestamp) - uniquely identifies each air-quality record by its city and observation time.
- Foreign keys: None used
- Uniqueness: Each city can only one record per timestamp which is enforced by the Primary key.
- Required columns: City and timestamp are NOT NULL.  We are including all Pollutants which can include missing data.  Also, Category and Score columns are required.  Possibly a daily.


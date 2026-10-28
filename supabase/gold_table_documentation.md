# Gold Air Quality Table

The gold_air_quality table stores cleaned and transformed hourly air-quality data for each city.

The gold table schema is defined in supabase/gold_air_quality.sql. Team members can use this SQL script to create the Gold table in their own Supabase testing projects.

- Copy and paste each SQL schema separately into the Supabase SQL Editor.
- Click Save and Run for each schema.
- In VSCode, run load.py to load the raw data, then run load_gold.py to transform/load the gold data.
- Once both scripts finish running, check Supabase, both tables should now include the data.

## Gold Table Keys and Requirements

- Primary key: (city, timestamp) - uniquely identifies each air-quality record by its city and observation time.
- Foreign keys: None used
- Uniqueness: Each city can only one record per timestamp which is enforced by the Primary key.

## Required Columns

| Field Name | Description | Data Type | Unit/Format | Source Field | Transformation Rule | Required?
| --- | --- | --- | ---| --- | --- | --- |
| city | Name of observed city | TEXT | City name (does not include State) | Input config used during extraction | map CITIES | YES |
| timestamp | Date and time of the record | TIMESTAMPTZ (datetime) | UTC timestamp | payload.list[].dt | Converted from Unix seconds to UTC datetime |  YES |
| aqi | OpenWeather Air Quality Index value | NUMERIC | Integer 1-5 | payload.list[].main.aqi | Rounded to closest integer during transformation | OPTIONAL |
| co | Carbon monoxide concentration | NUMERIC | µg/m³ | payload.list[].components.co | can be Null if missing data | OPTIONAL |
| no | Nitrogen monoxide concentration | NUMERIC | µg/m³ | payload.list[].components.no | can be Null if missing data | OPTIONAL |
| no2 | Nitrogen dioxide concentration | NUMERIC | µg/m³ | payload.list[].components.no2 | can be Null if missing data | OPTIONAL |
| o3 | Ozone concentration | NUMERIC | µg/m³ | payload.list[].components.o3 | can be Null if missing data | OPTIONAL |
| so2 | Sulfur dioxide concentration | NUMERIC | µg/m³ | payload.list[].components.so2 | can be Null if missing data | OPTIONAL |
| pm2_5 | Fine particulate matter concentration | NUMERIC | µg/m³ | payload.list[].components.pm2_5 | can be Null if missing data | OPTIONAL |
| pm10 | Particulate matter| NUMERIC | µg/m³ | payload.list[].components.pm10 | can be Null if missing data | OPTIONAL |
| nh3 | Ammonia concentration | NUMERIC | µg/m³ | payload.list[].components.nh3 | can be Null if missing data | OPTIONAL |
| category | based on AQI value | TEXT | Good, Fair, Moderate, Poor, Very Poor | OpenWeather website |  Map AQI values: 1 = Good, 2 = Fair, 3 = Moderate, 4 = Poor, 5 = Very Poor | OPTIONAL |
| score | Rolling average of AQI for the city | NUMERIC | Int, 1-5 | payload.list[].main.aqi | pandas rolling func | OPTIONAL |

## Rolling Aggregate: Score
The rolling aggregate calculates a rolling 24-hour average of AQI readings for each city. It updates with each recorded reading, using available data within the previous 24 hours, even when some hourly timestamps are missing.  Rounded to a whole number and stored in the score column to help user understand recent air quality trends.


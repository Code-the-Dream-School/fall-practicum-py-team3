# Gold Air Quality Table

The gold_air_quality table stores cleaned and transformed hourly air-quality data for each city.

The gold table schema is defined in supabase/gold_air_quality.sql. Team members can use this SQL script to create the Gold table in their own Supabase testing projects.

- Copy and paste each SQL schema separately into the Supabase SQL Editor.
- Click Save and Run for each schema.
- In VSCode, run load.py to load the raw data, then run load_gold.py to transform/load the gold data.
- Once both scripts finish running, check Supabase, both tables should now include the data.

If the table already exists from before `daily_aqi` was added, run this once in the SQL Editor:

```sql
ALTER TABLE gold_air_quality ADD COLUMN IF NOT EXISTS daily_aqi NUMERIC;
```

## Gold Table Keys and Requirements

- Primary key: (city, timestamp) - uniquely identifies each air-quality record by its city and observation time.
- Foreign keys: None used
- Uniqueness: Each city can only have one record per timestamp, which is enforced by the primary key.

## Missing and Malformed Values

A gold record is only written when every required field is present. If a raw reading is missing its city, timestamp, aqi, or any pollutant, `transform()` raises a `ValueError` instead of guessing a value. An aqi outside 1-5 is also rejected. Gold rows are never filled in or estimated, so every value in the table was actually reported by OpenWeather.

## Columns

| Field Name | Description                                                              | Data Type              | Unit/Format                           | Source Field                               | Transformation Rule                                            | Required? |
| ---------- | ------------------------------------------------------------------------ | ---------------------- | ------------------------------------- | ------------------------------------------ | -------------------------------------------------------------- | --------- |
| city       | Name of observed city                                                    | TEXT                   | City name (does not include State)    | Input config used during extraction        | map CITIES                                                     | YES       |
| timestamp  | Date and time of the record                                              | TIMESTAMPTZ (datetime) | UTC timestamp                         | payload.list[].dt                          | Converted from Unix seconds to UTC datetime                    | YES       |
| aqi        | OpenWeather Air Quality Index value                                      | NUMERIC                | Integer 1-5                           | payload.list[].main.aqi                    | Rounded to closest integer; rejected if missing or outside 1-5 | YES       |
| co         | Carbon monoxide concentration                                            | NUMERIC                | µg/m³                                 | payload.list[].components.co               | Stored as reported; row rejected if missing                    | YES       |
| no         | Nitrogen monoxide concentration                                          | NUMERIC                | µg/m³                                 | payload.list[].components.no               | Stored as reported; row rejected if missing                    | YES       |
| no2        | Nitrogen dioxide concentration                                           | NUMERIC                | µg/m³                                 | payload.list[].components.no2              | Stored as reported; row rejected if missing                    | YES       |
| o3         | Ozone concentration                                                      | NUMERIC                | µg/m³                                 | payload.list[].components.o3               | Stored as reported; row rejected if missing                    | YES       |
| so2        | Sulfur dioxide concentration                                             | NUMERIC                | µg/m³                                 | payload.list[].components.so2              | Stored as reported; row rejected if missing                    | YES       |
| pm2_5      | Fine particulate matter concentration                                    | NUMERIC                | µg/m³                                 | payload.list[].components.pm2_5            | Stored as reported; row rejected if missing                    | YES       |
| pm10       | Coarse particulate matter concentration                                  | NUMERIC                | µg/m³                                 | payload.list[].components.pm10             | Stored as reported; row rejected if missing                    | YES       |
| nh3        | Ammonia concentration                                                    | NUMERIC                | µg/m³                                 | payload.list[].components.nh3              | Stored as reported; row rejected if missing                    | YES       |
| category   | Name of the AQI level                                                    | TEXT                   | Good, Fair, Moderate, Poor, Very Poor | aqi                                        | 1 = Good, 2 = Fair, 3 = Moderate, 4 = Poor, 5 = Very Poor      | YES       |
| score      | AQI level for this hour, with a decimal for how far into the level it is | NUMERIC                | 1.00 to 5.99                          | components (so2, no2, pm10, pm2_5, o3, co) | Worst pollutant's position on OpenWeather's bands (see below)  | YES       |
| daily_aqi  | Average AQI over the previous 24 hours for this city                     | NUMERIC                | Decimal, 1.0 to 5.0                   | aqi                                        | Rolling 24-hour mean per city (see below)                      | YES       |

All pollutant concentrations come from OpenWeather in µg/m³ and are stored in the same unit, so no unit conversion is needed.

## Score

Score is the AQI for that hour, worked out from the pollutant readings, with a decimal showing how far into the level the reading is.

OpenWeather gives each pollutant its own range for every AQI level ([source](https://openweathermap.org/api/air-pollution)):

| Level       | SO2     | NO2     | PM10    | PM2.5 | O3      | CO          |
| ----------- | ------- | ------- | ------- | ----- | ------- | ----------- |
| 1 Good      | 0-20    | 0-40    | 0-20    | 0-10  | 0-60    | 0-4400      |
| 2 Fair      | 20-80   | 40-70   | 20-50   | 10-25 | 60-100  | 4400-9400   |
| 3 Moderate  | 80-250  | 70-150  | 50-100  | 25-50 | 100-140 | 9400-12400  |
| 4 Poor      | 250-350 | 150-200 | 100-200 | 50-75 | 140-180 | 12400-15400 |
| 5 Very Poor | 350+    | 200+    | 200+    | 75+   | 180+    | 15400+      |

For each pollutant, the score is its level plus how far through that level it is. For example, ozone at 57.5 is 96% of the way through Good (0-60), so it scores 1.95. Ozone at 60.5 has just entered Fair, so it scores 2.01. The row's score is the highest of these, because the worst pollutant is what sets the AQI. NO and NH3 are not part of OpenWeather's AQI, so they do not count toward the score.

The whole number of the score always matches `aqi`. OpenWeather rounds concentrations before sending them, so a reading shown exactly on a cutoff (ozone at 60.0, PM2.5 at 10.0) can belong to either level, and on rare hours particle readings come back as 0 even though OpenWeather's AQI still counts them. In those cases the score is kept inside the level OpenWeather assigned. In the current data this affects 58 of 281,385 rows. The decimal lets users rank cities and hours that share the same AQI level.

## Rolling Aggregate: daily_aqi

`daily_aqi` is the average AQI for the same city over the 24 hours ending at that row's timestamp. Every hourly row has a value, and it updates each hour as the window moves forward.

- **Window:** 24 hours by time, not 24 rows, so missing hours do not stretch the window.
- **Per city:** each city is averaged only with its own readings.
- **Start of the data:** the first readings average whatever is available so far, so the first day of a city's data uses fewer than 24 readings.
- **Not rounded:** the value keeps its decimals, so 2.67 stays 2.67.

This helps users see recent air quality trends. A single hour can spike, but `daily_aqi` shows whether the last day has been mostly clean or mostly polluted.

## How These Fields Support the Product Question

The Sprint 1 question asks how air quality compares across cities and over time, and what health guidance applies.

- **category** gives the plain-language level that each EPA-based health tip is tied to.
- **score** compares cities and hours within the same level, so two "Fair" cities can still be ranked.
- **daily_aqi** shows how air quality is changing over time, smoothing out single-hour spikes.

# Dataset and Product Decision

## Dataset

The team chose the Air Pollution API from OpenWeather.
LINK: https://openweathermap.org/api/air-pollution?collection=environmental

Why: It is free to start, covers any coordinates, returns hourly readings, and has history back to November 2020, so we have enough data to show trends.

Known limitation: OpenWeather estimates air pollution with models and satellite data. It does not report readings from ground monitoring stations, so it can miss very local pollution. We will state this on the dashboard.

### Alternatives considered

Anton's alternatives document compared OpenWeather with OpenAQ, Open-Meteo, AirNow and EPA AQS. We tested OpenAQ for Oklahoma City, and it does offer real station readings, but it costs more effort for this project:

- Stations differ by city, and each reports a different set of pollutants, so we would have to find and choose a good station for every city.
- Station data has gaps: some sensors stop reporting and some hours are missing.
- Readings come per sensor, so we would need a lookup from sensor ID to pollutant and units, and many more API calls.

OpenWeather returns every pollutant, with the same structure, for any coordinates, so the whole team can build against one predictable response. We chose reliability and simplicity over station-level accuracy.

Possible stretch goal: if time allows later, OpenAQ's public S3 archive could be added as a second source to compare station readings against OpenWeather's modeled values. It is not part of the current scope.

## Product Question

**Main question:** How does air quality compare across U.S. regions, and how does it change over time?

**Prioritized ideas** (we decide these now and do not add new ones in later weeks):

1. Which cities and regions have the best and worst air right now, and what health tip applies at that level?
2. How does air quality change over time within a city (hour of day, recent days, and further back)?
3. Which pollutants most often push a city into Poor or Very Poor?
4. When are pollution levels a potential concern, meaning how often does each city reach Poor or Very Poor?

## Scope

- **Geography:** United States only.
- **Cities:** Spread across the U.S. Census divisions so every region is represented. Final city list: [TBD, decide in the weekly sync].
- **Time range:** [TBD, decide after testing how far back the hourly data reaches. See Open Questions.]
- **Out of scope:** Other countries, forecasts, and station-based data sources.

## Data Contract

**Request:** latitude (lat), longitude (lon), start and end time (Unix timestamps).

**Response fields:**

| Field      | Meaning                                |
| ---------- | -------------------------------------- |
| dt         | Unix timestamp of the reading          |
| main.aqi   | Air quality index, 1 to 5              |
| components | CO, NO, NO2, O3, SO2, PM2.5, PM10, NH3 |

**AQI scale:** We use OpenWeather's 1 to 5 scale, not the U.S. EPA scale or other country-specific scales.

| Value | Label     |
| ----- | --------- |
| 1     | Good      |
| 2     | Fair      |
| 3     | Moderate  |
| 4     | Poor      |
| 5     | Very Poor |

The labels live in one lookup dictionary in code. The Transform step adds the label to each row.

**Pollutant units:** The API does not include units in the response. We store them as constants in code (OpenWeather lists all components in ug/m3; confirm against the docs before relying on this).

**Uniqueness:**

- API request: a response is identified by (lat, lon, start, end).
- Stored rows: one row per city per hour. Unique key is city plus timestamp.

## Database Decision

Choice: Supabase, because the whole team and our cloud deployment need to share one database. Connection details are stored in environment variables, never in GitHub.

## ETL Process

Extract: For each city, call the API with its coordinates and a time window. Save the raw response along with the request details and the time we retrieved it.

Transform: Flatten the response into one row per city per hour. Convert Unix timestamps to readable dates, add the city name, add the AQI label from the lookup, attach units from the constants, and handle missing values (keep the row and store the missing pollutant as null). An LLM then adds a short health tip to each record.

Load: Save the clean rows into Supabase. Use city plus timestamp as the unique key so rerunning the pipeline does not create duplicates.

## Dashboard

A Streamlit dashboard reads from the Supabase table. It lets the user pick a city, shows the latest air quality label and health tip, and charts pollutant levels over time. A city comparison view shows how locations differ, grouped by region.

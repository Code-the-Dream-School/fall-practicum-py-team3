# Dataset and Product Decision

## Dataset

The team chose the Air Pollution API from OpenWeather.
LINK: https://openweathermap.org/api/air-pollution?collection=environmental

Why: It is free to start, covers any coordinates, returns hourly readings, and has history back to November 2020, so we have enough data to show trends.

Known limitation: OpenWeather estimates air pollution with models and satellite data. It does not report readings from ground monitoring stations, so it can miss very local pollution. We will state this on the dashboard.

Possible stretch goal: if time allows later, OpenWeather has a geocoding API that converts a city name into latitude and longitude coordinates. This would allow the dashboard to use a search-style build.

## Product Question

**Main question:** How does air quality compare across U.S. regions, and how does it change over time?

**Prioritized ideas** (we decide these now and do not add new ones in later weeks):

1. Which cities and regions have the best and worst air, and what health tip applies at that level according to EPA guidelines?
2. How does air quality change over time within a city (day by day, over the full history)?

## Product Question(s)

How do air quality levels and dominant pollutants compare across 32 US cities, using daily OpenWeather readings from November 2020 to today, and what health guidance applies to the AQI levels each city reached based on EPA guidelines?

## Scope

- **Geography:** United States only.
- **Cities:** 32 cities spread across the U.S. so every region is represented.
- **Time range:** November 2020 (the start of OpenWeather's history) to today, about six years, with new data added daily after that.
- **Granularity:** One reading per city per day. OpenWeather returns hourly data, so we take one reading for each day [TBD, time of day].
- **Out of scope:** Other countries, forecasts, and station-based data sources.

## Data Needed

**Request:** latitude (lat), longitude (lon), start and end time (Unix timestamps).

**Response fields:**

| Field      | Meaning                                |
| ---------- | -------------------------------------- |
| dt         | Unix timestamp of the reading          |
| main.aqi   | Air quality index, 1 to 5              |
| components | CO, NO, NO2, O3, SO2, PM2.5, PM10, NH3 |

**AQI scale:** We use OpenWeather's 1 to 5 scale for the AQI levels, not the U.S. EPA scale or other country-specific scales. The health tips use EPA guidelines for each pollutant, so the tips are based on EPA guidance even though the AQI levels follow OpenWeather's scale.

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
- Stored rows: one row per city per day. Unique key is city plus date.

## Database Decision

Choice: Supabase, because the whole team and our cloud deployment need to share one database. Connection details are stored in environment variables, never in GitHub.

## ETL Process

Extract: For each city, call the API with its coordinates and a time window. Save the raw response along with the request details and the time we retrieved it.

Transform: Flatten the response into one row per city per day. Convert Unix timestamps to readable dates, add the city name, add the AQI label from the lookup, attach units from the constants, and handle missing values (keep the row and store the missing pollutant as null). An LLM then adds a short health tip to each record.

Load: Save the clean rows into Supabase. Use city plus date as the unique key so rerunning the pipeline does not create duplicates.

The full history is loaded once. After that, a scheduled AWS Lambda function makes the same API call to add each new day's data.

## Dashboard

A Streamlit dashboard reads from the Supabase table. It lets the user pick a city, shows the latest air quality label and health tip, and charts pollutant levels over time.

# Dataset and Product Decision

## Dataset

The team chose the Air Pollution API from OpenWeather.
LINK: https://openweathermap.org/api/air-pollution?collection=environmental

Why: It is free to start, covers any coordinates, returns hourly readings, and has history back to November 2020, so we have enough data to show trends.

## Product Question(s)

How do air quality levels and dominant pollutants compare across 20 US cities, 2 per Census division plus Alaska and Hawaii, using hourly OpenWeather data from the last 30 days, and what health guidance applies to the AQI levels each city reached based on EPA guidelines?

## Data Needed

The Historical Air Pollution API provides:

- AQI score (1-5)
- CO, NO, NO2, O3, SO2, PM2.5, PM10, NH3
- datetime (dt, Unix timestamp)

The API request needs:

- latitude (lat) and longitude (lon)
- start and end time (Unix timestamps)

## Database Decision

Choice: Supabase, because the whole team and our cloud deployment need to share one database. Connection details are stored in environment variables, never in GitHub.

## ETL Process

Extract: For each city, call the API with its coordinates and a time window. Save the raw response along with the request details and the time we retrieved it.

Transform: Flatten the response into one row per city per hour. Convert Unix timestamps to readable dates, add the city name, label the AQI score 1-5 (Good to Very Poor), and handle missing values. An LLM then adds a short health tip to each record.

Load: Save the clean rows into Supabase. Use city plus timestamp as a unique key so rerunning the pipeline does not create duplicates.

## Dashboard

A Streamlit dashboard reads from the Supabase table. It lets the user pick a city, shows the latest air quality label and health tip, and charts pollutant levels over time. A city comparison view shows how locations differ.

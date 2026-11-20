# Input Configuration

## Purpose
The pipeline requires configuration values that determine which air-quality data to retrieve from the OpenWeather Air Pollution API.

## Required Inputs
- Cities: A predefined list of cities with their latitude and longitude coordinates.
- Time Window: A start timestamp and end timestamp defining the period of air-quality to retrieve from the OpenWeather Air Pollution Historical API.
- API Credentials: The OpenWeather API key must be provided through an environment variable and should not be hardcoded or committed to GitHub.

## Cities Coordinates
Team has decided to use a preselected list of cities.  The dashboard will allow users to compare the air-quality of the different cities across the different divisions of the United States.

Each city in the configuration will include a city name, latitude, and longitude, which the pipeline will use to retrieve air-quality data from the OpenWeather API. 

Refer to cities.yaml


## Time Window
Our team will be extracting 1 year worth of historical data from each of the cities from the OpenWeather API.

OpenWeather has history back to November 2020, but we start with 1 year to keep the database small while the pipeline is new. The team agreed to extend the window once we know the database has room for more.

| Setting | Date | Unix Timestamp |
| --- | --- | --- |
|START | Oct 25, 2025, 00:00 UTC | 1761350400 |
| END | Oct 25, 2026, 00:00 UTC| 1792886400 |

Format: Unix timestamps in seconds, using UTC.


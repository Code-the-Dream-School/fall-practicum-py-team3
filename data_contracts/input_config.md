# Input Configuration

## Purpose
The pipeline requires configuration values that determine which air-quality data to retrieve from the OpenWeather Air Pollution API.

## Required Inputs
- Cities: A predefined list of cities with their latitude and longitude coordinates.
- Time Window: A start timestamp and end timestamp defining the period of air-quality to retrieve from the OpenWeather Air Pollution Historical API.
- API Credentials: The OpenWeather API key must be provided through an environment variable and should not be hardcoded or committed to GitHub.

## Cities Coordinates
Team has decided to use a preselected list of cities.  The dashboard will allow users to compare the air-quality of the different cities across the different divisions of the United States.

Each city in the configuration will include a city name, latitude, and longitude, which the pipeline will use to retrieve air-quality data from the OpenWeather API.  Coordinates will be recorded to 2 decimal places for consistency.


| Regions | Cities | LAT | LON |
| --- | --- | --- | --- |
| New England | Boston, MA | 42.36 | -71.06 |
| | Providence, RI | 41.83 | -71.42 |
| Mid-Atlantic | New York City, NY | 40.71 | -74.01 |
| | Philadelphia, PA | 39.95 | -75.17 |
| | Pittsburgh, PA | 40.44 | -80.00 |
| | Buffalo, NY | 42.89 | -78.88 |
| East North Central | Chicago, IL | 41.88 | -87.62 |
| | Detroit, MI | 42.33 | -83.05 |
| | Columbus, OH | 39.96 | -83.00 |
| | Milwaukee, WI | 43.04 | -87.91 |
| West North Central | Minneapolis, MN | 44.98 | -93.27 |
| | Kansas City, MO | 39.10 | -94.58 |
| | Omaha, NE | 41.26 | -95.94 |
| South Atlantic | Washington, DC | 38.91 | -77.04 |
| | Charlotte, NC | 35.23 | -80.84 |
| | Atlanta, GA | 33.75 | -84.39 |
| | Miami, FL | 25.76 | -80.19 |
| | Tampa, FL | 27.95 | -82.46 |
| East South Central | Birmingham, AL | 33.54 | -86.80 |
| | Memphis, TN | 35.15 | -90.05 |
| | Nashville, TN | 36.16 | -86.78 |
| West South Central | Houston, TX | 29.76 | -95.37 |
| | Dallas, TX | 32.78 | -96.80 |
| | Oklahoma City, OK | 35.47 | -97.52 |
| | El Paso, TX | 31.76 | -106.49 |
| Mountain | Phoenix, AZ | 33.45 | -112.07 |
| | Salt Lake City, UT | 40.76 | -111.89 |
| | Denver, CO | 39.74 | -104.98 |
| | Missoula, MT | 46.87 | -113.99 |
| Pacific | Los Angeles, CA | 34.05 | -118.24 |
| | Seattle, WA | 47.61 | -122.33 |
| | Honolulu, HI | 21.31 | -157.86 |
| | Anchorage, AK | 61.22 | -149.90 |


## Time Window
Our team will be extracting 1 year worth of historical data from each of the cities from the OpenWeather API.

OpenWeather has history back to November 2020, but we start with 1 year to keep the database small while the pipeline is new. The team agreed to extend the window once we know the database has room for more.

| Setting | Date | Unix Timestamp |
| --- | --- | --- |
|START | Oct 25, 2025, 00:00 UTC | 1761350400 |
| END | Oct 25, 2026, 00:00 UTC| 1792886400 |

Format: Unix timestamps in seconds, using UTC.


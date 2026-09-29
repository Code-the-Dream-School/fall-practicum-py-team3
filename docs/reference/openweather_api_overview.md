# OpenWeather API Overview

## Purpose

OpenWeather offers many products, but this practicum only requires the APIs available through its free-access API key. Use this guide to choose a project direction before your team starts building the extract layer.

> **No payment is required for this practicum.** Do not enter credit-card information or subscribe to One Call or another paid product. If OpenWeather asks for payment information, stop and return to one of the free-access API pages below or ask your mentor for help.

OpenWeather documents its current free-access options on its [pricing page](https://openweathermap.org/price). Product access and limits can change, so check that page and the individual API documentation if something behaves differently from this guide.

## Choose a primary API

Each team should choose **one primary API** that determines the main question its dashboard will answer. Air pollution is the recommended path because the original curriculum and project reference materials were designed around it, but teams may choose current weather or weather forecasts instead.

### Current weather

[Current Weather Data](https://openweathermap.org/api/current?collection=current_forecast) provides a snapshot of conditions for a location, including temperature, humidity, wind, clouds, visibility, and observed weather conditions.

Choose this direction if your dashboard should emphasize questions such as:

- What is the weather like in each city right now?
- Which cities are currently hottest, coldest, windiest, or most humid?
- How do current conditions compare across locations?

### Weather forecast

[5 Day / 3 Hour Forecast](https://openweathermap.org/api/forecast5) provides forecast data in three-hour intervals for five days.

Choose this direction if your dashboard should emphasize questions such as:

- How are conditions expected to change over the next five days?
- When are rain, high winds, or temperature changes expected?
- How do short-term forecasts compare across locations?

### Air pollution — recommended

[Air Pollution API](https://openweathermap.org/api/air-pollution?collection=environmental) provides current, forecast, and historical air-quality data, including an air-quality index and pollutant concentrations.

Choose this direction if your dashboard should emphasize questions such as:

- What is the current air quality in each city?
- Which pollutants are most elevated?
- How does air quality change across locations or over time?

The project also includes a more focused [OpenWeather Environmental API field reference](./openweather_environmental_api_fields_reference.md) for teams that choose this path.

## Supplementary APIs

These APIs can support the team's primary direction, but none is required. Keep the core project focused: implement one primary API first and add no more than one supplementary or second data API unless your mentor agrees that the scope is manageable.

### Weather Maps 1.0

[Weather Maps 1.0](https://openweathermap.org/api/weathermaps?collection=maps) provides map tiles for layers such as precipitation, clouds, pressure, temperature, and wind.

Consider it if a map layer would make the selected weather data easier to understand. It is a visual supplement, not a replacement for the primary data API.

### Geocoding

[Geocoding API](https://openweathermap.org/api/geocoding-api?collection=other) converts place names into latitude and longitude and can also perform reverse geocoding.

Consider it if the team wants users or configuration files to identify locations by city name. A team whose location input already includes coordinates may not need it.

### Weather Stations

[Weather Stations API](https://openweathermap.org/api/stations?collection=other) supports registering and managing personally owned weather stations and sending or retrieving their measurements.

Consider it only if the team has a clear station-related use case. It is not required to use current weather, forecast, or air-pollution data.

## Keep the choice focused

One well-understood API is enough for a strong project. A second API can be useful when it directly supports the dashboard goal, but every additional integration adds request logic, response fields, error cases, tests, and documentation.

Before implementation, agree on:

1. The primary API and the question the dashboard will answer.
2. The specific endpoint and response fields the project needs.
3. Whether one supplementary or second API adds enough value to justify the work.
4. How locations will be represented and whether geocoding is necessary.
5. What the team will intentionally leave out of the first version.

The team can revise this decision later, but it should finish one reliable extraction path before expanding the scope.

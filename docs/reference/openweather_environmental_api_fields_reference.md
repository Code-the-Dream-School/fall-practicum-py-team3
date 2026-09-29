# OpenWeather Environmental API Field Reference (Developer)

## Purpose
This document summarizes the OpenWeather Environmental Air Pollution API fields for all exposed endpoints in the Environmental collection:
- Current air pollution
- Forecast air pollution
- Historical air pollution

Source docs:
- https://openweathermap.org/api/air-pollution?collection=environmental
- https://openweathermap.org/api/air-pollution?collection=environmental#fields
- https://openweathermap.org/air-pollution-index-levels

## Base URL
https://api.openweathermap.org/data/2.5

## Endpoints

### 1) Current Air Pollution
GET /air_pollution

Use this endpoint to retrieve current air quality at a coordinate.

Query parameters:

| Field | Type | Required | Description | Example |
|---|---|---|---|---|
| lat | number | Yes | Latitude of target location. | 50.0 |
| lon | number | Yes | Longitude of target location. | 50.0 |
| appid | string | Yes | OpenWeather API key. | YOUR_API_KEY |

Example request:
https://api.openweathermap.org/data/2.5/air_pollution?lat=50&lon=50&appid=YOUR_API_KEY

### 2) Forecast Air Pollution
GET /air_pollution/forecast

Use this endpoint to retrieve forecasted air quality (OpenWeather states hourly forecast up to 4 days).

Query parameters:

| Field | Type | Required | Description | Example |
|---|---|---|---|---|
| lat | number | Yes | Latitude of target location. | 50.0 |
| lon | number | Yes | Longitude of target location. | 50.0 |
| appid | string | Yes | OpenWeather API key. | YOUR_API_KEY |

Example request:
https://api.openweathermap.org/data/2.5/air_pollution/forecast?lat=50&lon=50&appid=YOUR_API_KEY

### 3) Historical Air Pollution
GET /air_pollution/history

Use this endpoint to retrieve historical air quality for a UTC Unix-time range.

Query parameters:

| Field | Type | Required | Description | Example |
|---|---|---|---|---|
| lat | number | Yes | Latitude of target location. | 50.0 |
| lon | number | Yes | Longitude of target location. | 50.0 |
| start | integer | Yes | Start of range in Unix seconds (UTC). | 1606488670 |
| end | integer | Yes | End of range in Unix seconds (UTC). | 1606747870 |
| appid | string | Yes | OpenWeather API key. | YOUR_API_KEY |

Example request:
https://api.openweathermap.org/data/2.5/air_pollution/history?lat=50&lon=50&start=1606488670&end=1606747870&appid=YOUR_API_KEY

## Common Response Schema (All Three Endpoints)

Top-level fields:

| Field | Type | Description | Notes |
|---|---|---|---|
| coord | array[number, number] | Coordinates used in response payload. | Ordered as [lat, lon]. |
| list | array<object> | Time-indexed pollutant measurements. | One object per timestamp/sample. |

### list[] object

| Field | Type | Description | Notes |
|---|---|---|---|
| dt | integer | Observation/forecast timestamp in Unix seconds (UTC). | Convert to ISO-8601 in clients for display and joins. |
| main | object | AQI container object. | Currently exposes main.aqi. |
| components | object | Pollutant concentration values. | Units are micrograms per cubic meter (ug/m3). |

### list[].main

| Field | Type | Description | Values |
|---|---|---|---|
| aqi | integer | OpenWeather Air Quality Index category. | 1, 2, 3, 4, 5 |

AQI category meaning in OpenWeather scale:

| aqi | Category |
|---|---|
| 1 | Good |
| 2 | Fair |
| 3 | Moderate |
| 4 | Poor |
| 5 | Very Poor |

### list[].components

All component values are concentrations in ug/m3.

| Field | Type | What it is for | Notes |
|---|---|---|---|
| co | number | Carbon monoxide concentration for health and combustion-related pollution analysis. | Included in AQI logic on OpenWeather scale table. |
| no | number | Nitrogen monoxide concentration, useful for traffic/combustion diagnostics. | OpenWeather notes this does not affect AQI score directly. |
| no2 | number | Nitrogen dioxide concentration, commonly used in urban traffic pollution assessment. | Included in AQI logic on OpenWeather scale table. |
| o3 | number | Ozone concentration for photochemical smog and respiratory risk tracking. | Included in AQI logic on OpenWeather scale table. |
| so2 | number | Sulphur dioxide concentration, often tied to industrial/fuel sulfur emissions. | Included in AQI logic on OpenWeather scale table. |
| pm2_5 | number | Fine particulate matter (diameter <= 2.5 um), high health relevance for lungs and cardiovascular risk. | Included in AQI logic on OpenWeather scale table. |
| pm10 | number | Coarse particulate matter (diameter <= 10 um), used for dust and particulate burden monitoring. | Included in AQI logic on OpenWeather scale table. |
| nh3 | number | Ammonia concentration, useful for agricultural/industrial source context. | OpenWeather notes this does not affect AQI score directly. |

## Developer Implementation Notes

- Treat dt as UTC Unix seconds. Always convert using timezone-aware utilities.
- Use numeric parsing defensively (float for component values, int for dt/aqi).
- Expect list length to vary by endpoint and requested window.
- Preserve raw payloads for reproducibility and future schema expansion.
- Validate that start <= end for historical queries before calling API.
- Keep API keys out of source code and version control.

## Example Unified Response

```json
{
  "coord": [50.0, 50.0],
  "list": [
    {
      "dt": 1606482000,
      "main": {
        "aqi": 2
      },
      "components": {
        "co": 270.367,
        "no": 5.867,
        "no2": 43.184,
        "o3": 4.783,
        "so2": 14.544,
        "pm2_5": 13.448,
        "pm10": 15.524,
        "nh3": 0.289
      }
    }
  ]
}
```

## Change Management

If OpenWeather adds fields in the Environmental API, update this file and downstream schema mappings (raw, transform, and data dictionary) together to keep docs and implementation in sync.

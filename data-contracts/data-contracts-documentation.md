# Data Contracts

## Purpose
This document defines the agreements that the pipeline stages will depend on.  These contracts are subject to change as the project develops.

## OpenWeather Environmental API Field Reference
- coord: coordinates used in response payload.
- dt: date and time of observation, Unix, UTC.
- aqi (Air Quality Index):
    - 1 = Good
    - 2 = Fair
    - 3 = Moderate
    - 4 = Poor
    - 5 = Very Poor
- pollutants (measured in μg/m3):
    - co = Carbon monoxide
    - no = Nitrogen monoxide
    - no2 = Nitrogen dioxide
    - o3 = Ozone
    - so2 = Sulphur dioxide
    - pm2_5 = Fine particulate matter (diameter <= 2.5 μg)
    - pm10 = Coarse particulate matter (diameter <= 10 μg)
    - nh3 = Ammonia 

## 1.) Raw Schema
The raw schema represents the data received from the OpenWeather Air Pollution API before the transformation.
A stored raw record should include:
- The date and time the data was retrieved
- The API payload
- The request parameters used to retrieve the data

The raw API response is validated using Pydantic.  The raw schema can be accessed via schemas.py in folder.

## 2.)  Gold Schema
The Gold schema defines the cleaned, analysis-ready data.
Each Gold record represents one air quality observation for a city at a specific timestamp.  The nested API response is flattened into a single record containing the AQI and pollutant measurements.

The Gold schema can be viewed in the schemas.py file.  This is a first draft for the Gold schema and may be adjusted in future.

## 3.) Function Signatures
The pipeline will use the following stages:

### <u>extract()</u>
- Purpose: Retrieve Air Pollution data from the OpenWeather API.

- Inputs: Location/coordinate information, requested time window, API credentials retrieved from environment variables.

- Output: Raw API response.

- Error behavior: Pydantic validation errors should be raised when the API response does not match the expected schema. API/request errors should be handled without silently returning invalid data.

### <u>load_raw()</u>
- Purpose: Store the raw API response and retrieval context.

- Inputs: Validated raw record.

- Output: Confirmation/result of the raw data load.

- Error behavior: Database/load errors should be handled and reported.

### <u>transform()</u>
- Purpose: Convert validated raw data into the Gold schema.

- Inputs: Validated raw record.

- Output: Gold records.

- Error behavior: Invalid or unusable data should be handled rather than silently producing incorrect Gold records.

## 4.)  Design Rule
Each pipeline function should be independent and only require the information needed to perform its task.  Functions should not rely on a specific workflow tool, dashboard, database connection, or local computer setup.

Configuration and secrets should be managed through environment variables.  This allows the same functions to be reused in different environments, such as AWS Lambda.

## 5.)  Input Configuration
- TBD
- Team has so far decided to use cities within the United States.


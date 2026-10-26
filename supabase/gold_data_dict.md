# Gold Data Dictionary

## Purpose
To document the fields stored in the Gold Air Quality table, including their meanings, data types, units/format, source field/transformation rule, required status.

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
| category | TBD |
| score | TBD |

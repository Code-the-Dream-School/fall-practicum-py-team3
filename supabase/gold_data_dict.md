# Gold Data Dictionary

## Purpose
To document the fields stored in the Gold Air Quality table, including their meanings, data types, units/format, source field/transformation rule, required status.

| Field Name | Description | Data Type | Unit/Format | Source Field or Transformation Rule | Required?
| --- | --- | --- | ---| --- | --- |
| city | Name of observed city | TEXT | City name (does not include State) | Input config used during extraction | YES |
| timestamp | Date and time of the record | TIMESTAMPTZ (datetime) | UTC timestamp | Raw dt, converted from Unix seconds to UTC datetime | YES |



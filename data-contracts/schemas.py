from datetime import datetime
from pydantic import BaseModel, ValidationError

# =======================
# RAW SCHEMA
# =======================

"""
Raw schema for the OpenWeather Air Pollution API response.

Mirrors the API structure before transformation.
Pydantic validates the response at the API boundary.
The data will later be transformed into the Gold schema.
"""

class Main(BaseModel):
    aqi: float | None = None

class Coordinates(BaseModel):
    lat: float
    lon: float

class Components(BaseModel):
    co: float | None = None
    no: float | None = None
    no2: float | None = None
    o3: float | None = None
    so2: float | None = None
    pm2_5: float | None = None
    pm10: float | None = None
    nh3: float | None = None

class AirQualityRecord(BaseModel):
    dt: int
    main: Main
    components: Components

class AirQualityResponse(BaseModel):
    coord: Coordinates
    list: list[AirQualityRecord]

class RequestParameters(BaseModel):
    lat: float
    lon: float
    start: int
    end: int

# This should be in another file. There might be better ways to do this as well.
# What's important is that we have an easy way to lookup city by lat, lon.
# The Cities dictionary in extract.py is the reverse of this.
CITY_LOOKUP = {
    str(Coordinates(lat=38.90, lon=-77.04)): "Washington, DC",
    str(Coordinates(lat=61.22, lon=-149.90)): "Washington, DC",
}


class RawAirQuality(BaseModel):
    retrieved_at: datetime
    request_parameters: RequestParameters
    payload: AirQualityResponse

    # You can define a custom function on the class
    # This returns a list of dictionaries that you can use to make DB calls
    # You'll have to check if Supabase wants a JSON string, or a dictionary and whether it will auto-convert Python types into SQL types
    # I just have everything as a string becuase I was testing print statements
    def to_raw_schema(self):
        city = CITY_LOOKUP[str(self.payload.coord)]
        retrieved_at = str(self.retrieved_at.timestamp())
        return [
            {
                "city": city,
                "timestamp": str(record.dt),
                "aqi": str(record.main.aqi),
                "co": str(record.components.co),
                "no": str(record.components.no),
                "no2": str(record.components.no2),
                "o3": str(record.components.o3),
                "so2": str(record.components.so2),
                "pm2_5": str(record.components.pm2_5),
                "pm10": str(record.components.pm10),
                "nh3": str(record.components.nh3),
                "retrieved_at": retrieved_at,
            } for record in self.payload.list
        ]

# =======================
# RAW SCHEMA EXAMPLE
# =======================

raw_example = RawAirQuality(
    retrieved_at=datetime.now(),
    request_parameters=RequestParameters(
        lat=38.90,
        lon=-77.04,
        start=1606488670,
        end=1606747870
    ),
    payload=AirQualityResponse(
        coord=Coordinates(lat=38.90, lon=-77.04),
        list=[
            AirQualityRecord(
                dt=1606482000,
                main=Main(aqi=2),
                components=Components(
                    co=270.367,
                    no=5.867,
                    no2=43.184,
                    o3=4.783,
                    so2=14.544,
                    pm2_5=13.448,
                    pm10=15.524,
                    nh3=0.289
                )
            )
        ]
    )
)

# =======================
# GOLD SCHEMA
# =======================

"""
Gold Schema: Defines the cleaned, analysis-ready structure of the air quality data.
Subject to change.
Each record represents one air quality observation for a city at a specific timestamp.
The data is flattened from the nested API response and includes the AQI and all pollutant measurements.
"""

class GoldAirQuality(BaseModel):
    city: str
    timestamp: datetime
    aqi: int
    co: float
    no: float
    no2: float
    o3: float
    so2: float
    pm2_5: float
    pm10: float
    nh3: float

# =======================
# GOLD SCHEMA EXAMPLE
# =======================

gold_example = GoldAirQuality(
    city="Washington, DC",
    timestamp=datetime(2020, 11, 27, 17, 0),
    aqi=2,
    co=270.367,
    no=5.867,
    no2=0.5,
    o3=4.783,
    so2=14.544,
    pm2_5=13.448,
    pm10=15.524,
    nh3=0.289
)


if __name__ == "__main__":
    print(raw_example.to_raw_schema())

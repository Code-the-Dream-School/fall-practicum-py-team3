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
    
class RawAirQuality(BaseModel):
    retrieved_at: datetime
    request_parameters: RequestParameters
    payload: AirQualityResponse

def to_raw_schema(self):
        city = city[str(self.payload.coord)]
        retrieved_at = str(self.retrieved_at.timestamp())
        return [
            {
                "city": city,
                "timestamp": datetime(record.dt),
                "aqi": float(record.main.aqi),
                "co": float(record.components.co),
                "no": float(record.components.no),
                "no2": float(record.components.no2),
                "o3": float(record.components.o3),
                "so2": float(record.components.so2),
                "pm2_5": float(record.components.pm2_5),
                "pm10": float(record.components.pm10),
                "nh3": float(record.components.nh3),
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
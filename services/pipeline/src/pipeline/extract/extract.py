import requests, pytest
from datetime import datetime, timezone
from dotenv import dotenv_values
from pydantic import BaseModel
from unittest.mock import Mock, patch
import json

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[5] / "data-contracts"))

from schemas import RawAirQuality, RequestParameters




API_KEY: str = dotenv_values(".env").get("OPENWEATHER_API_KEY")

# Pydantic for validating the latitude, longitude, start, and end
class City(BaseModel):
    LAT: float
    LON: float
    START: int
    END: int

# instantiate the City class
# city = City(LAT=42.36,LON=-71.06,START=1760486400,END=1792108800)

CITIES = {
            "Boston": {"LAT": 42.36, "LON": -71.06},
            "Providence": {"LAT": 41.83, "LON": -71.42},
            "New York City": {"LAT": 40.71, "LON": -74.01},
            "Philadelphia": {"LAT": 39.95, "LON": -75.17},
            "Pittsburgh": {"LAT": 40.44, "LON": -80.00},
            "Buffalo": {"LAT": 42.89, "LON": -78.88},
            "Chicago": {"LAT": 41.88, "LON": -87.62},
            "Detroit": {"LAT": 42.33, "LON": -83.05},
            "Columbus": {"LAT": 39.96, "LON": -83.00},
            "Milwaukee": {"LAT": 43.04, "LON": -87.91},
            "Minneapolis": {"LAT": 44.98, "LON": -93.27},
            "Kansas City": {"LAT": 39.10, "LON": -94.58},
            "Omaha": {"LAT": 41.26, "LON": -95.94},
            "Washington DC": {"LAT": 38.91, "LON": -77.04},
            "Charlotte": {"LAT": 35.23, "LON": -80.84},
            "Atlanta": {"LAT": 33.75, "LON": -84.39},
            "Miami": {"LAT": 25.76, "LON": -80.19},
            "Tampa": {"LAT": 27.95, "LON": -82.46},
            "Birmingham": {"LAT": 33.54, "LON": -86.80},
            "Memphis": {"LAT": 35.15, "LON": -90.05},
            "Nashville": {"LAT": 36.16, "LON": -86.78},
            "Houston": {"LAT": 29.76, "LON": -95.37},
            "Dallas": {"LAT": 32.78, "LON": -96.80},
            "Oklahoma City": {"LAT": 35.47, "LON": -97.52},
            "El Paso": {"LAT": 31.76, "LON": -106.49},
            "Phoenix": {"LAT": 33.45, "LON": -112.07},
            "Salt Lake City": {"LAT": 40.76, "LON": -111.89},
            "Denver": {"LAT": 39.74, "LON": -104.98},
            "Missoula": {"LAT": 46.87, "LON": -113.99},
            "Los Angeles": {"LAT": 34.05, "LON": -118.24},
            "Seattle": {"LAT": 47.61, "LON": -122.33},
            "Honolulu": {"LAT": 21.31, "LON": -157.86},
            "Anchorage": {"LAT": 61.22, "LON": -149.90}
        }

START = 1760486400
END = 1792022400

# cache > prevent redundant requests for identical historical windows
_POLLUTION_CACHE = {} # in-memory dict > stores data['list'] for {lat, lon, start, end}
CACHE_TTL_SECONDS = 300 # 5 minutes before becoming stale

def clear_cache():
    _POLLUTION_CACHE.clear() # reset cache between tests

# Extract all the parameters and call the Historical Air Pollution API
# changed name of func from mock_extract to extract
def extract(city: City) -> RawAirQuality:
    # create cache key > check for valid cached data
    cache_key = f"{city.LAT},{city.LON},{city.START},{city.END}"
    now_ts = datetime.now(timezone.utc).timestamp()
    if cache_key in _POLLUTION_CACHE:
        cached_data, cached_time = _POLLUTION_CACHE[cache_key]
        if now_ts - cached_time < CACHE_TTL_SECONDS:
            # metadata = {
            #     "source": "http://api.openweathermap.org/data/2.5/air_pollution/history",
            #     "request_params": {
            #         "lat": city.LAT,
            #         "lon": city.LON,
            #         "start": city.START,
            #         "end": city.END,
            #     },
            #     "retrieved_at": datetime.now(timezone.utc).isoformat(),
            # }
            # changed to Pydantic instead of dict for cache
            return RawAirQuality(
                retrieved_at=datetime.now(timezone.utc),
                request_parameters=RequestParameters(
                    lat=city.LAT,
                    lon=city.LON,
                    start=city.START,
                    end=city.END,
                ),
                payload=cached_data
            ) 
        else:
            del _POLLUTION_CACHE[cache_key]  # invalidate stale entry
    
    try:
        # Assign .env variable
        api = API_KEY
        # Fetch historical air pollution data
        response = requests.get(f"http://api.openweathermap.org/data/2.5/air_pollution/history",
            params={
            "lat": city.LAT,
            "lon": city.LON,
            "start": city.START,
            "end": city.END,
            "appid": api
            }
        )

        response.raise_for_status()
        data = response.json()    # parse the JSON body into Python objects

        # If the connection's successful return the API's data
        if response.status_code == 200:
            # Return False if the data['list'] is empty
            if data['list'] == []:
                print("No air pollution records found.")

            metadata = {
                "source": "http://api.openweathermap.org/data/2.5/air_pollution/history",
                "request_params": {
                    "lat": city.LAT,
                    "lon": city.LON,
                    "start": city.START,
                    "end": city.END
                },
                "retrieved_at": datetime.now(timezone.utc).isoformat() # convert date object into a standardized string
            }
            
            # Pydantic RawAirQuality for validation instead of dict
            result = RawAirQuality(
                retrieved_at=datetime.now(timezone.utc),
                request_parameters=RequestParameters(
                        lat=city.LAT,
                        lon=city.LON,
                        start=city.START,
                        end=city.END,
                    ),
                payload=data
            )
            
            # store result in cache
            _POLLUTION_CACHE[cache_key] = (data, now_ts)
            
            return result

    # Except block for JSON errors
    except requests.exceptions.JSONDecodeError as err:
        print(f"Failed to decode JSON {err}")
        raise err
    
    
# save data to file
def write_to_json(city_name, result):
    filename = Path(
        f"./services/pipeline/src/pipeline/extract/cities_raw/"
        f"{city_name.lower().replace(' ', '_')}.json"
    )
    
    if filename.exists():
        return
    
    with open(filename, "w") as file:
        json.dump(result.model_dump(mode="json"), file)
    
    
    
    
if __name__ == "__main__":
    
    # loop for cities
    for name, coordinates in CITIES.items():
        city = City(
            LAT=coordinates["LAT"],
            LON=coordinates["LON"],
            START=START,
            END=END,
        )
        
        result = extract(city)
        
        write_to_json(name, result)
        
        print(f"{name}: {len(result.payload.list)} records saved")
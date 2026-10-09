import requests, os, json
import pandas as pd
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict
import unittest

# Pydantic for validating the API_KEY
class Settings(BaseSettings):
    API_KEY: str
    model_config = SettingsConfigDict(env_file="../../.env")
        
settings = Settings()

# Pydantic for validating the latititude, longitude, start, and end
class City(BaseModel):
    LAT: float
    LON: float
    START: int
    END: int
 
# instantiate the City class   
city = City(LAT=38.9,LON=77.04,START=1606488670,END=1606747870)

# Extract all the parameters and call the Historical Air Pollution API
def mock_extract(city: City):
    # Assign .env variable
    api = settings.API_KEY
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
   
    # If the connection's successful return the API's data
    if response.status_code == 200: 
        data = response.json()    # parse the JSON body into Python objects
        return data
    
    # If the connection isn't successful raise an error
    if response.status_code == 400 or response.status_code == 401 or response.status_code == 500:
        response.raise_for_status()
    else:
        response.raise_for_status()

if __name__ == '__main__':
    print(mock_extract(city))
import requests, os, json
import pandas as pd
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict
import unittest

class Settings(BaseSettings):
    API_KEY: str
    model_config = SettingsConfigDict(env_file="../../.env")
        
settings = Settings()
class City(BaseModel):
    LAT: float
    LON: float
    START: int
    END: int
    
city = City(LAT=38.9,LON=77.04,START=1606488670,END=1606747870)

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
   
    if response.status_code == 200: 
        data = response.json()    # parse the JSON body into Python objects
        return data
    if response.status_code == 400 or response.status_code == 401 or response.status_code == 500:
        response.raise_for_status()
    else:
        response.raise_for_status()

if __name__ == '__main__':
    print(mock_extract(city))
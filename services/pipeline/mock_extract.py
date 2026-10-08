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
    
city = City()

def mock_extract(lat, lon, start, end):
    # Assign .env variable
    api = settings.API_KEY
    # Fetch historical air pollution data
    response = requests.get(f"http://api.openweathermap.org/data/2.5/air_pollution/history?lat={lat}&lon={lon}&start={start}&end={end}&appid={api}")
    data = response.json()    # parse the JSON body into Python objects
    if response.status_code == 200:   
        return data
    else:
        return 'No data available'

if __name__ == '__main__':
    print(mock_extract(38.9,77.04,1606488670,1606747870))
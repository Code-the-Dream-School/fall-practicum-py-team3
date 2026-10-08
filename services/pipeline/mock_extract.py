import requests, os, json
import pandas as pd
# from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict
import unittest

class Settings(BaseSettings):
    LAT: float
    LON: float
    START: int
    END: int
    API_KEY: str


    model_config = SettingsConfigDict(env_file="../../.env")
        
settings = Settings()
# Assign .env variables
lat = settings.LAT
lon = settings.LON
start = settings.START
end = settings.END
api = settings.API_KEY

# Fetch historical air pollution data
response = requests.get(f"http://api.openweathermap.org/data/2.5/air_pollution/history?lat={lat}&lon={lon}&start={start}&end={end}&appid={api}")
data = response.json()    # parse the JSON body into Python objects

def mock_extract():
    if response.status_code == 200:   
        return data
    else:
        return 'No data available'
        
    return data

if __name__ == '__main__':
    print(mock_extract())
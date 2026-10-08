import requests, os, json
import pandas as pd
from dotenv import load_dotenv
import unittest

# Load in .env
load_dotenv()

# Assign .env variables
lat = os.getenv("LAT")
lon = os.getenv("LON")
start = os.getenv("START")
end = os.getenv("END")
api = os.getenv("API_KEY")

# Fetch historical air pollution data
response = requests.get(f"http://api.openweathermap.org/data/2.5/air_pollution/history?lat={lat}&lon={lon}&start={start}&end={end}&appid={api}")
data = response.json()    # parse the JSON body into Python objects

def mock_extract():
    if response.status_code == 200:   
        return data
    else:
        data = 'No data available'
        
    return data

if __name__ == '__main__':
    print(mock_extract())
import requests, pytest, os, json
import pandas as pd
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict
import unittest
from unittest.mock import Mock, patch



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
    try:
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
        data = response.json()    # parse the JSON body into Python objects
        
        # If the connection's successful return the API's data
        if response.status_code == 200:   
            # Return False if the data['list'] is empty
            if data['list'] == []:
                return False
            return data
        
        # If the connection isn't successful raise an error
        if response.status_code == 400 or response.status_code == 401 or response.status_code == 500:
            response.raise_for_status()
        
        # Left this for status codes outside of the ones above    
        else:
            response.raise_for_status()
            
    # Except block for JSON errors
    except requests.exceptions.JSONDecodeError as err:
        print(f"Failed to decode JSON {err}")
        raise err

# Mock Test 1 -- Validation
  
@patch("mock_extract_test.requests.get") # this temporarily replaces requests.get()
def test_mock_air(mock_requests): # parameter automatically supplied by @patch
    mock_test = Mock()
    mock_test.status_code = 200
    
    # When the extraction function calls response.json(), return the dictionary.
    mock_test.json.return_value = {
        "coord": {
            "lon": 67.9,
            "lat": -36.2
        },
        "list":[
            {
                "dt": 16526135192,
                "main":{
                    "aqi":3
                },
                "components":{
                    "co":222.94053649902347,
                    "no":0.02753197964450326,
                    "no2":0.3710350927815162,
                    "o3":49.68453078129,
                    "so2":0.4607496312354492,
                    "pm2_5":0.8,
                    "pm10":0.340438751643219,
                    "nh3":0.12069127561582794
                }
            }
        ]
    } 

    mock_requests.return_value = mock_test
    
    result = mock_extract(city)
    # assert the length of the result's "list" & compare it to a pollution records
    assert len(result["list"]) == 1

# Mock Test 2 -- Empty API Response

@patch("mock_extract_test.requests.get")   
def test_mock__empty_air(mock_requests): 
    mock_test = Mock()
    mock_test.status_code = 200
    
    # Empty list for the empty test
    mock_test.json.return_value = {
        "coord": {
            "lon": 67.9,
            "lat": -36.2
        },
        "list":[]
    } 

    mock_requests.return_value = mock_test
    result = mock_extract(city)
    assert result is False

# Mock Test 3 -- Unsuccessful HTTP Response

@patch("mock_extract_test.requests.get")   
def test_mock__http(mock_requests): 
    mock_test = Mock()
    mock_test.status_code = 500
    
    # raise status for the HTTPError
    mock_test.raise_for_status.side_effect = (
        requests.exceptions.HTTPError
    )
    
    mock_requests.return_value = mock_test
   
    # wrap with pytest.raises(same error as above)
    with pytest.raises(requests.exceptions.HTTPError):
        mock_extract(city)
    
# Mock Test 4 -- Invalid JSON
@patch("mock_extract_test.requests.get")   
def test_mock__json(mock_requests): 
    mock_test = Mock()
    mock_test.status_code = 200
    
    # raise status for the JSONDecodeError
    mock_test.json.side_effect = (
        requests.exceptions.JSONDecodeError(
            "Invalid JSON",
            "not-json",
            0
        )
    )
    
    mock_requests.return_value = mock_test
   
    with pytest.raises(requests.exceptions.JSONDecodeError):
        mock_extract(city)
        
if __name__ == '__main__':
    mock_extract(city)
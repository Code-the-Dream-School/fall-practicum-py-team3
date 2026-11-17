import requests
from datetime import datetime, timezone
from pydantic import BaseModel

import yaml

from pipeline.config import settings
import json

from pipeline.log import get_logger

logger = get_logger(__name__)
import time
from pathlib import Path

from pipeline.run_tracking import start_run, finish_run, fail_run, get_last_successful_run

import data_contracts.schemas as _schemas
RawAirQuality = _schemas.RawAirQuality
RequestParameters = _schemas.RequestParameters






# Pydantic for validating the latitude, longitude, start, and end
class City(BaseModel):
    LAT: float
    LON: float
    START: int
    END: int

# instantiate the City class
# city = City(LAT=42.36,LON=-71.06,START=1760486400,END=1792108800)

def _load_cities():
    path = Path(__file__).resolve().parents[1] / "cities.yaml"
    data = yaml.safe_load(path.read_text())
    return {
        entry["name"]: {"LAT": entry["lat"], "LON": entry["lon"]}
        for entry in data["cities"]
    }

CITIES = _load_cities()

START = 1761350400
END = 1792886400

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
        # Fetch historical air pollution data
        response = requests.get(f"http://api.openweathermap.org/data/2.5/air_pollution/history",
            params={
            "lat": city.LAT,
            "lon": city.LON,
            "start": city.START,
            "end": city.END,
            "appid": settings.openweather_api_key
            }
        )

        response.raise_for_status()
        data = response.json()    # parse the JSON body into Python objects

        # If the connection's successful return the API's data
        if response.status_code == 200:
            # Return False if the data['list'] is empty
            if data['list'] == []:
                logger.warning("No air pollution records found.")

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
    
    
##Chunking and caching logic for extracting all windows of data for a city
CHUNK_SECONDS = 365 * 24 * 60 * 60  # one year per API call, which is known to work
RETRIES = 3
RETRY_DELAY_SECONDS = 1


def raw_path(city_name):
    return Path(
        f"./services/pipeline/src/pipeline/extract/cities_raw/"
        f"{city_name.lower().replace(' ', '_')}.json"
    )


def chunk_windows(start, end, size=CHUNK_SECONDS):
    windows = []
    t = start
    while t < end:
        windows.append((t, min(t + size, end)))
        t += size
    return windows


def extract_all_windows(name, coords):
    """Pull START..END one year at a time, then merge into one result per city."""
    records = {}  # keyed by timestamp, so overlapping chunk edges don't duplicate
    base = None
    for win_start, win_end in chunk_windows(START, END):
        city = City(LAT=coords["LAT"], LON=coords["LON"], START=win_start, END=win_end)
        for attempt in range(1, RETRIES + 1):
            try:
                result = extract(city)
                break
            except requests.exceptions.RequestException as err:
                logger.warning("  %s %s-%s: attempt %s failed (%s)", name, win_start, win_end, attempt, err)
                if attempt == RETRIES:
                    raise
                time.sleep(5 * attempt)
        base = base or result
        for record in result.payload.list:
            records[record.dt] = record
        time.sleep(1)  # short pause between calls
    clear_cache()  # chunks are never reused, so don't let the cache grow
    merged = base.payload.model_copy(update={"list": [records[t] for t in sorted(records)]})
    return RawAirQuality(
        retrieved_at=datetime.now(timezone.utc),
        request_parameters=RequestParameters(lat=coords["LAT"], lon=coords["LON"], start=START, end=END),
        payload=merged,
    )
    
# incremental stuff
def get_incremental_window():
    """Calculate the next hourly extraction window."""
    last_run = get_last_successful_run()
    
    if last_run is None:
        raise ValueError("No successful previous run found.")
    
    last_end = int(
        datetime.fromisoformat(last_run["window_end"]).timestamp()
    )
    
    next_start = last_end + 3600 # 3600 for seconds in 1 hr
    
    # extraction of new start window
    current_hour = (
        int(datetime.now(timezone.utc).timestamp()) // 3600
    ) * 3600 
    
    next_end = current_hour - 3600
    
    if next_start > next_end:
        return None
    
    return next_start, next_end

# incremental stuff
def extract_incremental_window(name, coords, start, end):
    """Extract only new hourly data for one city."""
    city = City(
        LAT=coords["LAT"],
        LON=coords["LON"],
        START=start,
        END=end
    )
    
    for attempt in range(1, RETRIES + 1):
        try:
            return extract(city)
        
        except requests.exceptions.RequestException as err:
            print(f"{name}: attempt {attempt} failed ({err})")
            
            if attempt == RETRIES:
                raise
            
            time.sleep(RETRY_DELAY_SECONDS * attempt)
        
        

def has_window(name):
    """True if this city's file already covers START..END. A missing or unreadable file means fetch again."""
    path = raw_path(name)
    if not path.exists():
        return False
    try:
        params = json.loads(path.read_text())["request_parameters"]
    except (json.JSONDecodeError, KeyError):
        return False
    return params["start"] == START and params["end"] == END

def write_to_json(city_name, result):
    with open(raw_path(city_name), "w") as file:
        json.dump(result.model_dump(mode="json"), file)

def main():
    run_id = start_run(
        run_mode = "backfill",
        window_start = datetime.fromtimestamp(START, timezone.utc).isoformat(),
        window_end = datetime.fromtimestamp(END, timezone.utc).isoformat()
    )
    rows_extracted = 0
    
    try:
        for name, coordinates in CITIES.items():
            if has_window(name):
                print(f"{name}: already has the full window, skipping")
                continue
        
            result = extract_all_windows(name, coordinates)
            write_to_json(name, result)
        
            count = len(result.payload.list)
            rows_extracted += count
        
            print(f"{name}: {count} records saved")
        
        finish_run(
            run_id,
            rows_extracted=rows_extracted,
            rows_transformed=0,
            rows_loaded=0,
        )
        
        print("Extraction completed successfully.")
        
    except Exception as error:
        fail_run(
            run_id,
            error,
            rows_extracted=rows_extracted,
        )
        raise
    
if __name__ == "__main__":
    main()
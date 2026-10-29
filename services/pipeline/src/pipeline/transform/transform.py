"""Transform raw OpenWeather air-quality readings into gold records."""

import sys
from importlib import import_module
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[5] / "data_contracts"))
_schemas = import_module("schemas")
GoldAirQuality = _schemas.GoldAirQuality
RawAirQuality = _schemas.RawAirQuality

# AQI labels follow OpenWeather's 1-5 scale, not the U.S. EPA scale.
AQI_LABELS = {1: "Good", 2: "Fair", 3: "Moderate", 4: "Poor", 5: "Very Poor"}

POLLUTANTS = ("co", "no", "no2", "o3", "so2", "pm2_5", "pm10", "nh3")
REQUIRED = ("city", "timestamp", "aqi") + POLLUTANTS

# OpenWeather's AQI bands, µg/m³: the lower edge of levels 1-5.
# https://openweathermap.org/api/air-pollution
# NO and NH3 are not part of OpenWeather's AQI, so they are left out here too.
BANDS = {
    "so2": [0, 20, 80, 250, 350],
    "no2": [0, 40, 70, 150, 200],
    "pm10": [0, 20, 50, 100, 200],
    "pm2_5": [0, 10, 25, 50, 75],
    "o3": [0, 60, 100, 140, 180],
    "co": [0, 4400, 9400, 12400, 15400],
}


def aqi_category(aqi):
    """Return the OpenWeather label for an AQI level of 1 through 5."""
    if aqi is None:
        raise ValueError("aqi is required to determine a category")
    if aqi not in AQI_LABELS:
        raise ValueError(f"aqi must be 1 through 5, got {aqi}")
    return AQI_LABELS[aqi]


def transform(raw, city=None):
    """Turn raw readings into one gold record per hourly reading.

    `raw` is either a RawAirQuality response for `city`, or rows read from
    the raw_air_quality table, which already carry their own city.
    """
    frame = _to_frame(raw, city)
    if frame.empty:
        return []

    _reject_missing(frame)
    frame = _standardize(frame)
    frame = _derive(frame)
    frame = _add_rolling_aggregate(frame)

    columns = ["city", "timestamp", "aqi", *POLLUTANTS, "category", "score", "aqi_24h_avg"]
    return [GoldAirQuality(**row) for row in frame[columns].to_dict(orient="records")]


def _to_frame(raw, city):
    """Both kinds of input become the same flat columns."""
    if not isinstance(raw, RawAirQuality):
        return pd.DataFrame(raw)

    if city is None:
        raise ValueError("city is required when transforming a RawAirQuality response")

    rows = [record.model_dump() for record in raw.payload.list]
    frame = pd.json_normalize(rows)
    if frame.empty:
        return frame

    # "main.aqi" -> "aqi", "components.pm2_5" -> "pm2_5"
    frame = frame.rename(columns=lambda name: name.split(".")[-1])
    frame["city"] = city
    frame["timestamp"] = pd.to_datetime(frame["dt"], unit="s", utc=True)
    return frame


def _reject_missing(frame):
    missing_columns = [name for name in REQUIRED if name not in frame.columns]
    if missing_columns:
        raise ValueError(f"missing columns: {', '.join(missing_columns)}")

    missing_values = [name for name in REQUIRED if frame[name].isna().any()]
    if missing_values:
        raise ValueError(f"missing values in required fields: {', '.join(missing_values)}")


def _standardize(frame):
    frame = frame.copy()
    frame["timestamp"] = pd.to_datetime(frame["timestamp"], utc=True).map(
        lambda stamp: stamp.to_pydatetime()
    )
    frame["aqi"] = pd.to_numeric(frame["aqi"]).round().astype(int)
    for pollutant in POLLUTANTS:
        frame[pollutant] = pd.to_numeric(frame[pollutant]).astype(float)
    return frame


def _derive(frame):
    frame = frame.copy()

    out_of_range = ~frame["aqi"].isin(AQI_LABELS)
    if out_of_range.any():
        bad = sorted(frame.loc[out_of_range, "aqi"].unique())
        raise ValueError(f"aqi must be 1 through 5, got {bad}")

    frame["category"] = frame["aqi"].map(AQI_LABELS)



    # Worst pollutant's position on OpenWeather's own scale: the whole number is
    # the level and the decimal shows progress through the band.


    # OpenWeather rounds concentrations before sending them, so a reading shown
    # exactly on a cutoff band value may really sit on either side, and some hours report
    # particles as 0. Keep the score inside the level OpenWeather assigned so
    # score and aqi never disagree.

    sub_indices = pd.DataFrame(
        {name: [_sub_index(value, edges) for value in frame[name]] for name, edges in BANDS.items()},
        index=frame.index,
    )


    score = sub_indices.max(axis=1).clip(lower=frame["aqi"], upper=frame["aqi"] + 0.99)
    frame["score"] = (score * 100).astype(int) / 100
    return frame

    
    # A value exactly on an edge stays in the lower level (ozone at 60 is Good),
    # which is how OpenWeather assigns its own AQI.

def _sub_index(value, edges):
    """Level plus progress through it, e.g. 2.25 = a quarter of the way through Fair."""
    level = max(1, sum(value > edge for edge in edges))
    lower = edges[level - 1]
    if level < len(edges):
        upper = edges[level]
    else:
        # Very Poor has no upper edge; reuse the width of the Poor band.
        upper = lower + (lower - edges[level - 2])
    return level + min((value - lower) / (upper - lower), 0.99)


def _add_rolling_aggregate(frame):
    """Average AQI over the previous 24 hours, per city."""
    frame = frame.sort_values(["city", "timestamp"]).copy()

    rolled = (
        frame.assign(timestamp=pd.to_datetime(frame["timestamp"], utc=True))
        .set_index("timestamp")
        .groupby("city")["aqi"]
        .rolling("24h", min_periods=1)
        .mean()
    )
    frame["aqi_24h_avg"] = rolled.to_numpy()
    return frame
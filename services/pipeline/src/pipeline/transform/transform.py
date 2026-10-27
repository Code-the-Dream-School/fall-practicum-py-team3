"""Transform raw OpenWeather air-quality responses into gold records."""

import sys
from importlib import import_module
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[5] / "data_contracts"))
_schemas = import_module("schemas")
GoldAirQuality = _schemas.GoldAirQuality

# AQI labels follow OpenWeather's 1-5 scale, not the U.S. EPA scale.
AQI_LABELS = {1: "Good", 2: "Fair", 3: "Moderate", 4: "Poor", 5: "Very Poor"}

POLLUTANTS = ("co", "no", "no2", "o3", "so2", "pm2_5", "pm10", "nh3")
REQUIRED = ("aqi",) + POLLUTANTS



def aqi_category(aqi):
    """Return the OpenWeather label for an AQI level of 1 through 5."""
    if aqi is None:
        raise ValueError("aqi is required to determine a category")
    if aqi not in AQI_LABELS:
        raise ValueError(f"aqi must be 1 through 5, got {aqi}")
    return AQI_LABELS[aqi]


def transform(raw, city):
    """Flatten a raw response into one gold record per hourly reading."""
    frame = _flatten(raw)
    if frame.empty:
        return []

    _reject_missing(frame)
    frame = _standardize(frame, city)
    frame = _derive(frame)

    columns = ["city", "timestamp", "aqi", *POLLUTANTS, "category", "score"]
    return [GoldAirQuality(**row) for row in frame[columns].to_dict(orient="records")]


def _flatten(frame_source):
    """Nested main/components objects become flat columns."""
    rows = [record.model_dump() for record in frame_source.payload.list]
    frame = pd.json_normalize(rows)
    # "main.aqi" -> "aqi", "components.pm2_5" -> "pm2_5"
    return frame.rename(columns=lambda name: name.split(".")[-1])


def _reject_missing(frame):
    missing = [name for name in REQUIRED if frame[name].isna().any()]
    if missing:
        raise ValueError(f"missing values in required fields: {', '.join(missing)}")


def _standardize(frame, city):
    frame = frame.copy()
    frame["city"] = city
    frame["timestamp"] = pd.to_datetime(frame["dt"], unit="s", utc=True).map(
        lambda stamp: stamp.to_pydatetime()
    )
    frame["aqi"] = frame["aqi"].round().astype(int)
    frame[list(POLLUTANTS)] = frame[list(POLLUTANTS)].astype(float)
    return frame


def _derive(frame):
    frame = frame.copy()

    out_of_range = ~frame["aqi"].isin(AQI_LABELS)
    if out_of_range.any():
        bad = sorted(frame.loc[out_of_range, "aqi"].unique())
        raise ValueError(f"aqi must be 1 through 5, got {bad}")

    frame["category"] = frame["aqi"].map(AQI_LABELS)
    # TODO: score is still TBD in gold_data_dict.md. Mirroring aqi keeps the
    # schema satisfied without inventing a metric.
    frame["score"] = frame["aqi"].astype(float)
    return frame
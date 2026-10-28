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
def _sub_index(value, edges):
    """Level plus progress through it, e.g. 2.25 = a quarter of the way through Fair."""
    level = sum(value >= edge for edge in edges)
    lower = edges[level - 1]
    if level < len(edges):
        upper = edges[level]
    else:
        # Very Poor has no upper edge; reuse the width of the Poor band.
        upper = lower + (lower - edges[level - 2])
    return min(level + (value - lower) / (upper - lower), 5.99)


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

    # Worst pollutant's position on OpenWeather's own scale, so the whole
    # number always matches aqi and the decimal shows progress through the band.
    sub_indices = pd.DataFrame(
        {name: [_sub_index(value, edges) for value in frame[name]] for name, edges in BANDS.items()},
        index=frame.index,
    )
    frame["score"] = (sub_indices.max(axis=1) * 100).astype(int) / 100
    return frame
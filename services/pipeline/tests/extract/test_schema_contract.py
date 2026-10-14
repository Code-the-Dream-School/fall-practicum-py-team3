import sys
from pathlib import Path

import pytest
from pydantic import ValidationError

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "data-contracts"))

from schemas import AirQualityResponse

REC = {
    "dt": 1606482000,
    "main": {"aqi": 2},
    "components": {"co": 270.367, "no": 5.867, "no2": 0.5, "o3": 4.783,
                   "so2": 14.544, "pm2_5": 13.448, "pm10": 15.524, "nh3": 0.289},
}


def test_valid_record():
    r = AirQualityResponse.model_validate({"coord": [-77.04, 38.9], "list": [REC]})
    assert r.list[0].main.aqi == 2


def test_missing_pollutant_is_null():
    rec = {**REC, "components": {"co": 1.0}}
    r = AirQualityResponse.model_validate({"coord": [-77.04, 38.9], "list": [rec]})
    assert r.list[0].components.o3 is None


def test_wrong_type_rejected():
    rec = {**REC, "main": {"aqi": "high"}}
    with pytest.raises(ValidationError):
        AirQualityResponse.model_validate({"coord": [-77.04, 38.9], "list": [rec]})


@pytest.mark.xfail(reason="contract has coord as list; the real API returns a dict")
def test_real_api_coord_shape():
    AirQualityResponse.model_validate(
        {"coord": {"lon": -77.04, "lat": 38.9}, "list": [REC]})
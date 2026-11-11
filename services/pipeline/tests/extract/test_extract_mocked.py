import pytest
import requests
from pydantic import ValidationError
from unittest.mock import Mock, patch

from pipeline.extract.extract import extract, City

LAT, LON, START, END = 38.9, -77.04, 1606488670, 1606747870

GOOD = {
    "coord": {"lon": LON, "lat": LAT},
    "list": [{
        "dt": 1606482000,
        "main": {"aqi": 2},
        "components": {"co": 270.367, "no": 5.867, "no2": 0.5, "o3": 4.783,
                       "so2": 14.544, "pm2_5": 13.448, "pm10": 15.524, "nh3": 0.289},
    }],
}


def make_city():
    return City(LAT=LAT, LON=LON, START=START, END=END)


def fake_response(status=200, data=None):
    r = Mock()
    r.status_code = status
    r.json.return_value = data
    r.raise_for_status.return_value = None
    return r


@pytest.fixture(autouse=True)
def fake_key(monkeypatch):
    monkeypatch.setattr("pipeline.extract.extract.settings.openweather_api_key", "fake-key", raising=False)
    from pipeline.config import settings
    monkeypatch.setattr(settings, "openweather_api_key", "fake-key")
    from pipeline.extract.extract import clear_cache
    clear_cache()


@patch("requests.get")
def test_successful_extract(mock_get):
    mock_get.return_value = fake_response(data=GOOD)
    result = extract(make_city())

    assert len(result.payload.list) == 1
    assert result.payload.list[0].main.aqi == 2
    assert result.request_parameters.lat == LAT
    assert result.request_parameters.lon == LON
    assert result.request_parameters.start == START
    assert result.request_parameters.end == END
    assert result.retrieved_at is not None

    params = mock_get.call_args.kwargs["params"]
    assert params["appid"] == "fake-key"
    assert params["lat"] == LAT and params["lon"] == LON


def test_invalid_type():
    with pytest.raises(ValidationError):
        City(LAT="abc", LON=LON, START=START, END=END)


@patch("requests.get")
def test_empty_list(mock_get):
    mock_get.return_value = fake_response(data={"coord": GOOD["coord"], "list": []})
    result = extract(make_city())
    assert result.payload.list == []


@patch("requests.get")
def test_http_error(mock_get):
    r = fake_response(status=500)
    r.raise_for_status.side_effect = requests.exceptions.HTTPError("boom")
    mock_get.return_value = r
    with pytest.raises(requests.exceptions.HTTPError):
        extract(make_city())


@patch("requests.get")
def test_invalid_json(mock_get):
    r = fake_response()
    r.json.side_effect = requests.exceptions.JSONDecodeError("bad", "doc", 0)
    mock_get.return_value = r
    with pytest.raises(requests.exceptions.JSONDecodeError):
        extract(make_city())


@patch("requests.get")
def test_missing_list_key(mock_get):
    mock_get.return_value = fake_response(data={"coord": GOOD["coord"]})
    with pytest.raises(KeyError):
        extract(make_city())
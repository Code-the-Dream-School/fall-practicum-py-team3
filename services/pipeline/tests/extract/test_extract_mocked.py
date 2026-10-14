import pytest
import requests
from pydantic import ValidationError
from unittest.mock import Mock, patch

from . import test_extract as ex

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
    return ex.City(LAT=LAT, LON=LON, START=START, END=END)


def fake_response(status=200, data=None):
    r = Mock()
    r.status_code = status
    r.json.return_value = data
    return r


@pytest.fixture(autouse=True)
def fake_key(monkeypatch):
    # extract reads API_KEY at import time, so patch the module variable
    monkeypatch.setattr(ex, "API_KEY", "fake-key")


# Successful end-to-end extract
@patch("requests.get")
def test_successful_extract(mock_get):
    mock_get.return_value = fake_response(data=GOOD)
    result = ex.mock_extract(make_city())

    assert len(result["raw_data"]["list"]) == 1
    assert result["raw_data"]["list"][0]["main"]["aqi"] == 2
    assert result["metadata"]["request_params"] == {
        "lat": LAT, "lon": LON, "start": START, "end": END}
    assert "retrieved_at" in result["metadata"]

    params = mock_get.call_args.kwargs["params"]
    assert params["appid"] == "fake-key"
    assert params["lat"] == LAT and params["lon"] == LON
    assert "fake-key" not in str(result["metadata"])   # key never leaks into output


# Invalid input
def test_invalid_type():
    with pytest.raises(ValidationError):
        ex.City(LAT="abc", LON=LON, START=START, END=END)


@pytest.mark.xfail(reason="City has no range validation yet")
@pytest.mark.parametrize("lat,lon", [(95, 0), (-95, 0), (0, 181), (0, -181)])
def test_out_of_range_coordinates(lat, lon):
    with pytest.raises(ValidationError):
        ex.City(LAT=lat, LON=lon, START=START, END=END)


@pytest.mark.xfail(reason="No START < END check yet")
def test_start_after_end():
    with pytest.raises(ValidationError):
        ex.City(LAT=LAT, LON=LON, START=END, END=START)


# Empty / unsuccessful / malformed
@patch("requests.get")
def test_empty_list(mock_get):
    mock_get.return_value = fake_response(data={"coord": GOOD["coord"], "list": []})
    result = ex.mock_extract(make_city())
    assert result["raw_data"]["list"] == []
    assert "metadata" in result


@patch("requests.get")
def test_http_error(mock_get):
    r = fake_response(status=401)
    r.raise_for_status.side_effect = requests.exceptions.HTTPError
    mock_get.return_value = r
    with pytest.raises(requests.exceptions.HTTPError):
        ex.mock_extract(make_city())


@patch("requests.get")
def test_invalid_json(mock_get):
    r = fake_response()
    r.json.side_effect = requests.exceptions.JSONDecodeError("bad", "not-json", 0)
    mock_get.return_value = r
    with pytest.raises(requests.exceptions.JSONDecodeError):
        ex.mock_extract(make_city())


@patch("requests.get")
def test_missing_list_key(mock_get):
    mock_get.return_value = fake_response(data={"coord": GOOD["coord"]})
    with pytest.raises(KeyError):       
        ex.mock_extract(make_city())


# Missing API key
@pytest.mark.xfail(reason="extract does not check for a missing key yet")
@patch("requests.get")
def test_missing_api_key(mock_get, monkeypatch):
    monkeypatch.setattr(ex, "API_KEY", None)
    mock_get.return_value = fake_response(data=GOOD)
    with pytest.raises(Exception):
        ex.mock_extract(make_city())
    mock_get.assert_not_called()        # no request should go out without a key
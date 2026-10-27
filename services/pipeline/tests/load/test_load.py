from datetime import datetime, timezone
from pathlib import Path
import sys
import pytest
from pydantic import ValidationError

# ---------------------------------------------------------------------------- #
# setup / sample data

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "data_contracts"))
sys.path.insert(0, str(ROOT / "services" / "pipeline" / "src"))

import pipeline
from schemas import (
    AirQualityRecord,
    AirQualityResponse,
    Components,
    Coordinates,
    GoldAirQuality,
    Main,
    RawAirQuality,
    RequestParameters,
)

aqi_category = getattr(pipeline, "aqi_category", None)
load = getattr(pipeline, "load", None)
transform = getattr(pipeline, "transform", None)

requires_load = pytest.mark.skipif(
    not callable(load), reason="pipeline load function is not implemented"
)
requires_transform = pytest.mark.skipif(
    not callable(transform), reason="pipeline transform function is not implemented"
)
requires_load_transform = pytest.mark.skipif(
    not callable(load) or not callable(transform),
    reason="pipeline load/transform functions are not implemented",
)
requires_category = pytest.mark.skipif(
    not callable(aqi_category),
    reason="pipeline aqi_category function is not implemented",
)

CITY = "Washington, DC"
DT_1 = 1606482000  # 2020-11-27 13:00:00 UTC
DT_2 = DT_1 + 3600  # one hour later
POLLUTANTS = ["co", "no", "no2", "o3", "so2", "pm2_5", "pm10", "nh3"]


def make_record(dt=DT_1, aqi=2) -> AirQualityRecord:
    return AirQualityRecord(
        dt=dt,
        main=Main(aqi=aqi),
        components=Components(
            co=270.367,
            no=5.867,
            no2=43.184,
            o3=4.783,
            so2=14.544,
            pm2_5=13.448,
            pm10=15.524,
            nh3=0.289,
        ),
    )


def make_raw(records) -> RawAirQuality:
    return RawAirQuality(
        retrieved_at=datetime(2020, 12, 1, 12, 0),
        request_parameters=RequestParameters(
            lat=38.90, lon=-77.04, start=1606488670, end=1606747870
        ),
        payload=AirQualityResponse(
            coord=Coordinates(lat=38.90, lon=-77.04), list=records
        ),
    )


@pytest.fixture
def raw_two_records():
    return make_raw([make_record(DT_1, aqi=2), make_record(DT_2, aqi=3, pm2_5=30.0)])


# ---------------------------------------------------------------------------- #
# load / transform


@requires_transform
def test_transform_output_contract(raw_two_records):
    result = transform(raw_two_records, CITY)

    # 2 items > instance of GoldAirQuality > output matches schema's fields
    assert len(result) == 2
    assert all(isinstance(r, GoldAirQuality) for r in result)
    assert all(set(r.model_dump()) == set(GoldAirQuality.model_fields) for r in result)

    # check first record > second is distinct >  values are not mixed up between rows
    first, second = result
    assert first.city == CITY
    assert first.timestamp == datetime(2020, 11, 27, 13, 0, tzinfo=timezone.utc)
    assert first.aqi == 2
    assert (first.co, first.no, first.no2, first.o3) == (270.367, 5.867, 43.184, 4.783)
    assert (first.so2, first.pm2_5, first.pm10, first.nh3) == (
        14.544,
        13.448,
        15.524,
        0.289,
    )
    assert second.timestamp == datetime(2020, 11, 27, 14, 0, tzinfo=timezone.utc)
    assert second.aqi == 3
    assert second.pm2_5 == 30.0


@requires_load_transform
def test_load_stores_transformed_records(raw_two_records):
    store: dict = {}
    expected = transform(raw_two_records, CITY)
    inserted = load(expected, store)

    # 2 items > instances of GoldAirQuality
    assert inserted == 2
    assert len(store) == 2
    assert all(isinstance(row, GoldAirQuality) for row in store.values())

    # sort by timestamp > check if identical
    stored_rows = sorted(
        (row.model_dump() for row in store.values()), key=lambda row: row["timestamp"]
    )
    expected_rows = sorted(
        (row.model_dump() for row in expected), key=lambda row: row["timestamp"]
    )
    assert stored_rows == expected_rows


# ---------------------------------------------------------------------------- #
# idempotency


@requires_load_transform
def test_loading_same_raw_data_twice_creates_no_duplicates(raw_two_records):
    store: dict = {}

    first = load(transform(raw_two_records, CITY), store)
    snapshot = dict(store)
    second = load(transform(raw_two_records, CITY), store)

    assert first == 2
    assert second == 0  # nothing new on second call
    assert len(store) == 2
    assert store == snapshot  # contents unchanged after second call


@requires_load_transform
def test_same_timestamp_for_different_cities_is_not_a_duplicate():
    store: dict = {}
    raw = make_raw([make_record()])

    load(transform(raw, "Washington, DC"), store)
    load(transform(raw, "Baltimore, MD"), store)

    assert len(store) == 2


# ---------------------------------------------------------------------------- #
# empty input


@requires_transform
def test_transform_empty_payload_returns_empty_list():
    # handle passing RawAirQuality object with empty list into transform
    assert transform(make_raw([]), CITY) == []


@requires_load
def test_load_empty_list_inserts_nothing():
    # handle passing empty list into load step
    store: dict = {}
    assert load([], store) == 0
    assert store == {}


# ---------------------------------------------------------------------------- #
# missing / malformed fields


def test_raw_schema_rejects_record_missing_dt():
    # dict with missing `dt` field
    bad = {"main": {"aqi": 2}, "components": {"co": 1.0}}
    with pytest.raises(ValidationError):
        AirQualityRecord.model_validate(bad)


def test_raw_schema_rejects_malformed_types():
    # string for latitude > then a dict missing the `list` field
    with pytest.raises(ValidationError):
        Coordinates.model_validate({"lat": "number", "lon": -77.04})
    with pytest.raises(ValidationError):
        AirQualityResponse.model_validate({"coord": {"lat": 1.0, "lon": 2.0}})


@requires_transform
def test_transform_rejects_record_with_missing_aqi():
    # create raw record with `aqi=None`, but Gold requires an `int`
    raw = make_raw(
        [AirQualityRecord(dt=DT_1, main=Main(aqi=None), components=Components(co=1.0))]
    )
    with pytest.raises(ValueError):
        transform(raw, CITY)


@pytest.mark.parametrize("field", POLLUTANTS)
@requires_transform
def test_transform_rejects_record_with_missing_pollutant(field):
    # set each pollutant in POLLUTANTS to `None`
    raw = make_raw([make_record(**{field: None})])
    with pytest.raises(ValueError):
        transform(raw, CITY)


# ---------------------------------------------------------------------------- #
# category and score


# parametrize with scores and expected category strings > confirm boundaries
@pytest.mark.parametrize(
    "aqi, expected",
    [
        (1, "Good"),  # lower boundary
        (2, "Fair"),
        (3, "Moderate"),
        (4, "Poor"),
        (5, "Very Poor"),  # upper boundary
    ],
)
@requires_category
def test_aqi_category_for_known_scores(aqi, expected):
    assert aqi_category(aqi) == expected


# values outside of 1–5
@pytest.mark.parametrize("aqi", [0, 6, -1, 100])
@requires_category
def test_aqi_category_rejects_out_of_range_scores(aqi):
    with pytest.raises(ValueError):
        aqi_category(aqi)


# handle when `None` is passed to category function
@requires_category
def test_aqi_category_rejects_none():
    with pytest.raises((ValueError, TypeError)):
        aqi_category(None)


# transform record > 1 and  5 > score in Gold row should equal raw score at both ends
@pytest.mark.parametrize("aqi", [1, 5])
@requires_load_transform
def test_transform_preserves_boundary_scores(aqi):
    (row,) = transform(make_raw([make_record(aqi=aqi)]), CITY)
    assert row.aqi == aqi
    assert aqi_category(row.aqi) == {1: "Good", 5: "Very Poor"}[aqi]

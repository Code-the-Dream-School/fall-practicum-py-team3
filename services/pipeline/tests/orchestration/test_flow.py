import importlib.util
from pathlib import Path
import sys
import pytest

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "services" / "pipeline" / "src"))

FLOW_PATH = (
    ROOT / "services" / "pipeline" / "src" / "pipeline" / "orchestration" / "flow.py"
)
FLOW_SPEC = importlib.util.spec_from_file_location(
    "pipeline_flow_under_test", FLOW_PATH
)
flow_module = importlib.util.module_from_spec(FLOW_SPEC)
FLOW_SPEC.loader.exec_module(flow_module)

RAW_RECORD = {
    "city": "Test City",
    "timestamp": "2020-11-27T13:00:00+00:00",
    "aqi": 2,
    "co": 270.367,
    "no": 5.867,
    "no2": 43.184,
    "o3": 4.783,
    "so2": 14.544,
    "pm2_5": 13.448,
    "pm10": 15.524,
    "nh3": 0.289,
    "retrieved_at": "2020-12-01T12:00:00",
}


class ExtractedRecords:
    def to_raw_schema(self, city_name):
        return [{**RAW_RECORD, "city": city_name}]


# pytest built-in fixtures:
# monkeypatch > temporarily replace dependencies > test flow logic (not dependency behavior)
# caplog > capture Python's logging output for duration of test


# ---------------------------------------------------------------------------- #
def prepare_flow(monkeypatch):
    monkeypatch.setattr(
        flow_module, "extract_city", lambda city_name, city: ExtractedRecords()
    )
    monkeypatch.setattr(flow_module, "load_records", lambda records: len(records))
    monkeypatch.setattr(flow_module, "enrich_records", lambda records: records)


def test_pipeline_succeeds(monkeypatch):
    prepare_flow(monkeypatch)

    result = flow_module.run_pipeline(
        mode="test",
        inputs={"Test City": {"LAT": 38.9, "LON": -77.04}},
        start=1,
        end=2,
    )

    assert result == {
        "status": "success",
        "mode": "test",
        "counts": {"extract": 1, "load": 1, "transform": 1, "enrichment": 1},
    }


def test_pipeline_reports_failure(monkeypatch, caplog):
    prepare_flow(monkeypatch)

    def fail_transform(records):
        raise ValueError("transform rejected invalid records")

    monkeypatch.setattr(flow_module, "transform_records", fail_transform)

    with pytest.raises(ValueError, match="transform rejected invalid records"):
        flow_module.run_pipeline(
            mode="test",
            inputs={"Test City": {"LAT": 38.9, "LON": -77.04}},
            start=1,
            end=2,
        )

    assert "Pipeline failed during transform" in caplog.text

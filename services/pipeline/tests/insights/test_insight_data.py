import sys
from pathlib import Path
from types import SimpleNamespace

import pytest
ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "services" / "pipeline" / "src"))

from pipeline.insight_data import (  
    PAGE_SIZE,
    get_gold_records,
    get_unenriched_gold,
    select_insight_inputs,
)


class InMemoryQuery:

    def __init__(self, rows, error=None):
        self._rows, self._error = list(rows), error
        self._order, self._lo, self._hi = [], 0, None

    def select(self, *_):
        return self

    def eq(self, col, val):
        self._rows = [r for r in self._rows if r.get(col) == val]
        return self

    def gte(self, col, val):
        self._rows = [r for r in self._rows if r.get(col) >= val]
        return self

    def lte(self, col, val):
        self._rows = [r for r in self._rows if r.get(col) <= val]
        return self

    def order(self, col):
        self._order.append(col)
        return self

    def range(self, lo, hi):
        self._lo, self._hi = lo, hi
        return self

    def execute(self):
        if self._error:
            raise self._error
        rows = sorted(self._rows, key=lambda r: tuple(r[c] for c in self._order))
        end = None if self._hi is None else self._hi + 1
        return SimpleNamespace(data=rows[self._lo:end])


class InMemoryClient:
    def __init__(self, tables, error=None):
        self._tables, self._error = tables, error

    def table(self, name):
        return InMemoryQuery(self._tables.get(name, []), self._error)


def make_gold_row(city, ts, **extra):
    return {"city": city, "timestamp": ts, "category": "Fair", "aqi": 2,
            "aqi_24h_avg": 2.0, "pm2_5": 5.0, **extra}


def test_returns_rows_for_city_only():
    client = InMemoryClient({"gold_air_quality": [
        make_gold_row("Boston", "2024-01-01"),
        make_gold_row("Chicago", "2024-01-01"),
    ]})
    rows = get_gold_records(client, city="Boston")
    assert [r["city"] for r in rows] == ["Boston"]


def test_date_range_filter():
    client = InMemoryClient({"gold_air_quality": [
        make_gold_row("Boston", "2024-01-01"),
        make_gold_row("Boston", "2024-01-02"),
        make_gold_row("Boston", "2024-01-03"),
    ]})
    rows = get_gold_records(client, "Boston", start="2024-01-02", end="2024-01-02")
    assert [r["timestamp"] for r in rows] == ["2024-01-02"]


def test_no_rows_returns_empty_list():
    assert get_gold_records(InMemoryClient({"gold_air_quality": []}), city="Boston") == []


def test_pagination_returns_every_row():
    n = PAGE_SIZE + 5
    rows = [make_gold_row("Boston", f"2024-{i:05d}") for i in range(n)]
    result = get_gold_records(InMemoryClient({"gold_air_quality": rows}), city="Boston")
    assert len(result) == n


def test_unenriched_skips_rows_with_insight():
    client = InMemoryClient({
        "gold_air_quality": [
            make_gold_row("Boston", "2024-01-01"),
            make_gold_row("Boston", "2024-01-02"),
        ],
        "daily_insight": [
            {"city": "Boston", "timestamp": "2024-01-01", "insight_text": "Fair air."},
        ],
    })
    rows = get_unenriched_gold(client)
    assert [r["timestamp"] for r in rows] == ["2024-01-02"]


def test_row_with_empty_insight_text_counts_as_unenriched():
    client = InMemoryClient({
        "gold_air_quality": [make_gold_row("Boston", "2024-01-01")],
        "daily_insight": [
            {"city": "Boston", "timestamp": "2024-01-01", "insight_text": None},
        ],
    })
    assert len(get_unenriched_gold(client)) == 1


def test_insight_inputs_keep_nulls():
    row = make_gold_row("Boston", "2024-01-01", pm2_5=None, extra_column="ignored")
    inputs = select_insight_inputs(row)
    assert inputs["pm2_5"] is None
    assert "extra_column" not in inputs
    assert inputs["city"] == "Boston"


def test_database_error_is_raised():
    client = InMemoryClient({}, error=RuntimeError("db down"))
    with pytest.raises(RuntimeError):
        get_gold_records(client)
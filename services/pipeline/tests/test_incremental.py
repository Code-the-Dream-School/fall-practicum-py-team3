import pipeline.extract.extract as extract_module
import pytest

# ----------------------------------------------------
# TEST 1: check new data extraction window calculation
def test_incremental_starts_after_last_successful_run(monkeypatch):
    monkeypatch.setattr(
        extract_module,
        "get_last_successful_run",
        lambda: {
            "window_end": "2026-10-25T00:00+00:00"
        },
    )
    
    start, end = extract_module.get_incremental_window()
    
    # start an hr after previous successful run
    assert start == 1792890000
    
    # uses completed hourly timestamps
    assert end >= start
    assert end % 3600 == 0
    
# ----------------------------------------------------
# TEST 2:
def test_incremental_window_without_previous_run(monkeypatch):
    monkeypatch.setattr(
        extract_module,
        "get_last_successful_run",
        lambda: None,
    )
    
    with pytest.raises(ValueError):
        extract_module.get_incremental_window()
        
# ----------------------------------------------------
# on Supabase, create a sql query with the following (uncomment in SQL Editor):
# SELECT city, timestamp, COUNT(*)
# FROM raw_air_quality
# GROUP BY city, timestamp
# HAVING COUNT(*) > 1;
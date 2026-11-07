import pandas as pd
import pipeline.load.load_insight as load_module

class FakeSupabase:
    def __init__(self):
        self.batches = []
        
    def table(self, table_name):
        self.table_name = table_name
        return self
    
    def upsert(self, records, on_conflict):
        self.batches.append(records)
        return self
    
    def execute(self):
        return self

# helper func
def make_records(hours, date="2026-10-15"):
    records = []
    
    for hour in range(hours):
        records.append({
            "city": "Boston",
            "timestamp": f"{date}T{hour:02d}:00:00+00:00",
            "category": "Moderate",
            "aqi_24_avg": 3,
        })
        
    return records

# ==============================================
# TEST 1: empty records
def test_empty_gold_records(monkeypatch):
    fake_supabase = FakeSupabase()
    
    monkeypatch.setattr(load_module, "supabase", fake_supabase)
    monkeypatch.setattr(
        load_module, "get_gold_records", lambda client: []
    )
    
    load_module.load_insight()
    
    assert fake_supabase.batches == []
    
# ==============================================
# TEST 2: skip days with less than 18 hours
def test_skips_days_with_less_than_18_hours(monkeypatch):
    fake_supabase = FakeSupabase()
    records = make_records(17)
    
    monkeypatch.setattr(load_module, "supabase", fake_supabase)
    monkeypatch.setattr(
        load_module, "get_gold_records", lambda client: records
    )
    
    load_module.load_insight()
    
    assert fake_supabase.batches == []
    
# ==============================================
# TEST 3: latest record and aqi as integer
def test_uses_latest_record(monkeypatch):
    fake_supabase = FakeSupabase()
    records = make_records(18)
    
    records[-1]["category"] = "Very Poor"
    records[-1]["aqi_24h_avg"] = 4.6
    
    monkeypatch.setattr(load_module, "supabase", fake_supabase)
    monkeypatch.setattr(
        load_module, "get_gold_records", lambda client: records
    )
    
    load_module.load_insight()
    
    loaded_record = fake_supabase.batches[0][0]
    
    assert loaded_record["timestamp"] == records[-1]["timestamp"]
    assert loaded_record["category"] == "Very Poor"
    assert loaded_record["aqi_24h_avg"] == 5
    

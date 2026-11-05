import pytest

from pipeline.enrichment import enrichment

# mocked llm call 
enrich_record = getattr(enrichment, "enrich_record", None)
call_llm = getattr(enrichment, "call_llm", None)

requires_enrichment = pytest.mark.skipif(
    not callable(enrich_record) or not callable(call_llm),
    reason="enrichment functions are not implemented yet",
)

# ============================================
# TEST 1: enrichment.py with mock llm response
@requires_enrichment
def test_enrich_record_with_mock_llm(monkeypatch):
    # fake llm response
    def fake_call_llm(record):
        return {
            "insight_text": "Air quality in Boston was moderate."
        }
        
    # replace real llm call with fake
    monkeypatch.setattr(enrichment, "call_llm", fake_call_llm)
    
    record = {
        "city": "Boston",
        "aqi_24h_avg": 2.5
    }

    result = enrichment.enrich_record(record)
    
    assert result["insight_text"] == "Air quality in Boston was moderate."
    
# ============================================
# TEST 2: skipped records
@requires_enrichment
def test_skip_already_enriched_record(monkeypatch):
    # track whether llm gets called
    calls = []
    
    def fake_call_llm(record):
        calls.append(record)
        return {"insight_text": "Fake insight"}
    
    monkeypatch.setattr(enrichment, "call_llm", fake_call_llm)
    
    record = {
        "city": "Boston",
        "aqi_24h_avg": 2.5,
        "enriched_at": "2026-11-03T10:00:00Z",
    }
    
    enrichment.enrich_record(record)
    
    # llm should not be called for an already enriched record
    assert calls == []
    
# ============================================
# TEST 3: idempotency
@requires_enrichment
def test_no_duplicate_enrichment(monkeypatch):
    calls = []
    
    def fake_call_llm(record):
        calls.append(record)
        return {"insight_text": "Air quality in Boston was moderate on November 5th."}
    
    monkeypatch.setattr(enrichment, "call_llm", fake_call_llm)
    
    record = {
        "city": "Boston",
        "timestamp": "2026-11-05",
        "aqi_24h_avg": 2.5,
        "enriched_at": None,
    }

    first_result = enrichment.enrich_record(record)
    second_result = enrichment.enrich_record(first_result)
    
    assert len(calls) == 1
    
# ============================================
# TEST 4: handle llm failure
@requires_enrichment
def test_llm_failure(monkeypatch):
    def fake_call_llm(record):
        raise Exception("LLM request failed")
        
    monkeypatch.setattr(enrichment, "call_llm", fake_call_llm)
        
    record = {
        "city": "Boston",
        "timestamp": "2026-11-05",
        "aqi_24h_avg": 2.5,
        "enriched_at": None,
    }
        
    result = enrichment.enrich_record(record)
        
    assert result["enriched_at"] is None
    assert result["enrichment_error"] == "LLM request failed"
        
# ============================================
# TEST 5: handle empty input

@requires_enrichment
def test_empty_records():
    result = enrichment.enrich_records([])
    
    assert result == []
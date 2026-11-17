import json
from types import SimpleNamespace

import pytest

from pipeline.enrichment import enrichment as en 

GOOD_TEXT = "Boston's air was in the Fair range on November 5, with a 24-hour average AQI of 2.0."


def make_record(**extra):
    record = {
        "city": "Boston",
        "timestamp": "2026-11-05T00:00:00+00:00",
        "aqi_24h_avg": 2.0,
        "category": "Fair",
        "enriched_at": None,
    }
    record.update(extra)
    return record


class InMemoryQuery:
    """Mimics the Supabase query chain used by run_enrichment."""

    def __init__(self, client):
        self._client = client
        self._lo, self._hi = 0, None
        self._payload = None

    def select(self, *_):
        return self

    def is_(self, *_):
        return self

    def order(self, *_):
        return self

    def range(self, lo, hi):
        self._lo, self._hi = lo, hi
        return self

    def upsert(self, payload, **_):
        self._payload = payload
        return self

    def execute(self):
        if self._payload is not None:
            self._client.saved.extend(self._payload)
            return SimpleNamespace(data=self._payload)
        end = None if self._hi is None else self._hi + 1
        return SimpleNamespace(data=self._client.rows[self._lo:end])


class InMemoryClient:
    """Stands in for the Supabase client, so tests need no key or network."""

    def __init__(self, rows):
        self.rows = rows
        self.saved = []

    def table(self, name):
        return InMemoryQuery(self)


@pytest.fixture
def run_log(monkeypatch):
    """Replaces run tracking, so tests never talk to the pipeline_runs table."""
    log = SimpleNamespace(finished=None, failed=None)
    monkeypatch.setattr(en, "start_run", lambda: 1)
    monkeypatch.setattr(en, "finish_run", lambda run_id, **kw: setattr(log, "finished", kw))
    monkeypatch.setattr(
        en, "fail_run",
        lambda run_id, error, **kw: setattr(log, "failed", (str(error), kw)),
    )
    return log


@pytest.fixture
def no_api_key(monkeypatch):
    monkeypatch.setattr(en, "settings", SimpleNamespace(openai_api_key=None))


# a good reply
def test_good_reply_is_used(monkeypatch):
    monkeypatch.setattr(en, "call_llm", lambda record: {"insight_text": GOOD_TEXT})
    result = en.enrich_record(make_record())
    assert result["insight_text"] == GOOD_TEXT
    assert result["insight_source"] == "llm"
    assert result["model"] == en.MODEL
    assert result["enrichment_error"] is None
    assert result["enriched_at"] is not None


# API failure
def test_api_failure_is_recorded_and_left_for_next_run(monkeypatch):
    def raise_timeout(record):
        raise TimeoutError("timed out")

    monkeypatch.setattr(en, "call_llm", raise_timeout)
    result = en.enrich_record(make_record())
    assert result["enriched_at"] is None
    assert result["enrichment_error"] == "timed out"
    assert result.get("insight_text") is None


# invalid responses
def test_invalid_json_reply_uses_template(monkeypatch):
    def bad_json(record):
        raise json.JSONDecodeError("bad", "not json", 0)

    monkeypatch.setattr(en, "call_llm", bad_json)
    result = en.enrich_record(make_record())
    assert result["insight_source"] == "template"
    assert result["enrichment_error"] is None
    assert result["enriched_at"] is not None


@pytest.mark.parametrize("reply", [
    {},
    {"insight_text": None},
    {"insight_text": ""},
    {"insight_text": "   "},
    {"insight_text": 123},
    {"insight_text": "x" * 301},
    {"insight_text": "Boston had Fair air. It was a calm day."},
    {"insight_text": "Boston's air was Fair and nobody should worry."},
    ["not", "a", "dict"],
])
def test_unusable_reply_uses_template(monkeypatch, reply):
    monkeypatch.setattr(en, "call_llm", lambda record: reply)
    result = en.enrich_record(make_record())
    assert result["insight_source"] == "template"
    assert result["model"] is None
    assert result["enrichment_error"] is None
    assert result["enriched_at"] is not None
    assert "Fair" in result["insight_text"]


# missing or invalid data: the LLM is never called 
@pytest.mark.parametrize("value", [None, "high", float("nan"), 0, 6, True])
def test_bad_aqi_skips_llm_and_records_reason(monkeypatch, value):
    calls = []
    monkeypatch.setattr(en, "call_llm", lambda r: calls.append(r) or {"insight_text": GOOD_TEXT})
    result = en.enrich_record(make_record(aqi_24h_avg=value))
    assert calls == []
    assert result["enriched_at"] is None
    assert "aqi_24h_avg" in result["enrichment_error"]


def test_missing_city_skips_llm(monkeypatch):
    calls = []
    monkeypatch.setattr(en, "call_llm", lambda r: calls.append(r) or {"insight_text": GOOD_TEXT})
    result = en.enrich_record(make_record(city=None))
    assert calls == []
    assert result["enrichment_error"] == "missing city"


# missing API key
def test_missing_api_key_stops_the_batch_with_a_clear_message(no_api_key):
    with pytest.raises(en.LLMConfigError, match="API key"):
        en.enrich_records([make_record()])


def test_call_llm_without_key_raises_clear_error(no_api_key):
    with pytest.raises(en.LLMConfigError, match="API key"):
        en.call_llm(make_record())


def test_call_llm_uses_the_client_it_is_given():
    captured = {}

    def create(**kwargs):
        captured.update(kwargs)
        reply = SimpleNamespace(content=json.dumps({"insight_text": GOOD_TEXT}))
        return SimpleNamespace(choices=[SimpleNamespace(message=reply)])

    fake_client = SimpleNamespace(chat=SimpleNamespace(completions=SimpleNamespace(create=create)))
    result = en.call_llm(make_record(), client=fake_client)
    assert result == {"insight_text": GOOD_TEXT}
    assert captured["model"] == en.MODEL
    assert captured["response_format"] == {"type": "json_object"}


# one bad record never stops the batch 
def test_one_failing_record_does_not_stop_the_batch(monkeypatch):
    def fake_llm(record):
        if record["city"] == "Denver":
            raise RuntimeError("boom")
        return {"insight_text": f"{record['city']}'s air was in the Fair range on November 5, "
                                f"with a 24-hour average AQI of 2.0."}

    monkeypatch.setattr(en, "call_llm", fake_llm)
    records = [make_record(city="Boston"), make_record(city="Denver"), make_record(city="Chicago")]
    results = en.enrich_records(records)
    assert [r["city"] for r in results] == ["Boston", "Denver", "Chicago"]
    assert results[0]["insight_source"] == "llm"
    assert results[1]["enriched_at"] is None
    assert "boom" in results[1]["enrichment_error"]
    assert results[2]["insight_source"] == "llm"


def test_unexpected_error_is_caught_by_the_batch(monkeypatch):
    def boom(record):
        if record["city"] == "Denver":
            raise ValueError("bad record")
        return {**record, "enriched_at": "done"}

    monkeypatch.setattr(en, "enrich_record", boom)
    results = en.enrich_records([make_record(city="Boston"), make_record(city="Denver")])
    assert results[0]["enriched_at"] == "done"
    assert results[1]["enriched_at"] is None
    assert results[1]["enrichment_error"] == "unexpected error: bad record"


# run_enrichment (saving and run tracking)
def test_run_enrichment_saves_every_record_even_when_one_fails(monkeypatch, run_log, capsys):
    monkeypatch.setattr(en, "call_llm", lambda record: {"insight_text": GOOD_TEXT})
    client = InMemoryClient([make_record(), make_record(city="Denver", aqi_24h_avg=None)])
    results = en.run_enrichment(client)
    out = capsys.readouterr().out
    assert len(results) == 2
    assert len(client.saved) == 2
    denver = [r for r in client.saved if r["city"] == "Denver"][0]
    assert denver["enriched_at"] is None
    assert denver["enrichment_error"] == "missing aqi_24h_avg"
    assert run_log.finished["rows_extracted"] == 2
    assert run_log.finished["rows_loaded"] == 2
    assert run_log.failed is None
    assert "failed 1" in out
    assert "missing aqi_24h_avg" in out


def test_run_enrichment_with_nothing_to_do(run_log, capsys):
    client = InMemoryClient([])
    assert en.run_enrichment(client) == []
    assert "Nothing to enrich." in capsys.readouterr().out
    assert run_log.finished["rows_extracted"] == 0
    assert client.saved == []


def test_run_enrichment_with_missing_key_fails_the_run_and_saves_nothing(run_log, no_api_key):
    client = InMemoryClient([make_record()])
    with pytest.raises(en.LLMConfigError):
        en.run_enrichment(client)
    assert "API key" in run_log.failed[0]
    assert run_log.finished is None
    assert client.saved == []
    
    
# single-sentence check
@pytest.mark.parametrize("text", [
    "Boston was Fair.",
    "Boston was Fair",
    "Boston was Fair!  ",
    "AQI was 2.0 in Boston.",
    "Chicago in the U.S. Midwest was Fair.",
    "St. Louis air was Fair.",
    "Washington, D.C. was Fair today.",
])
def test_single_sentence_is_accepted(text):
    assert en.is_single_sentence(text) is True


@pytest.mark.parametrize("text", [
    "Boston was Fair. Denver was Good.",
    "Boston was Fair! It was calm.",
    "Boston was Fair? Yes. Good air.",
])
def test_several_sentences_are_rejected(text):
    assert en.is_single_sentence(text) is False


def test_reply_with_an_abbreviation_is_used(monkeypatch):
    text = "Air in the U.S. Northeast was Fair, with a 24-hour average AQI of 2.0."
    monkeypatch.setattr(en, "call_llm", lambda record: {"insight_text": text})
    result = en.enrich_record(make_record())
    assert result["insight_source"] == "llm"
    assert result["insight_text"] == text
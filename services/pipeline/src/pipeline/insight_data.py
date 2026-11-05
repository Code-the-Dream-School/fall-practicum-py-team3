##Retrieve gold data for LLM insights.

PAGE_SIZE = 1000 

# Fields sent to the LLM prompt.
INSIGHT_FIELDS = (
    "city", "timestamp", "category", "aqi", "aqi_24h_avg",
    "pm2_5", "pm10", "o3", "no2", "so2", "co", "score",
)


def _apply_filters(query, city, start, end):
    if city:
        query = query.eq("city", city)
    if start:
        query = query.gte("timestamp", start)
    if end:
        query = query.lte("timestamp", end)
    return query.order("city").order("timestamp")


def _fetch_all(client, table, city, start, end):
    rows, offset = [], 0
    while True:
        query = _apply_filters(client.table(table).select("*"), city, start, end)
        batch = query.range(offset, offset + PAGE_SIZE - 1).execute().data or []
        rows.extend(batch)
        if len(batch) < PAGE_SIZE:
            return rows
        offset += PAGE_SIZE


def get_gold_records(client, city=None, start=None, end=None):
    """All gold rows, optionally filtered by city and a timestamp range."""
    return _fetch_all(client, "gold_air_quality", city, start, end)


def get_unenriched_gold(client, city=None, start=None, end=None):
    gold = get_gold_records(client, city, start, end)
    done = {
        (r["city"], r["timestamp"])
        for r in _fetch_all(client, "daily_insight", city, start, end)
        if r.get("insight_text")
    }
    return [r for r in gold if (r["city"], r["timestamp"]) not in done]


def select_insight_inputs(row):
    """The measurements to send to the LLM for one gold row. Missing values stay None."""
    return {field: row.get(field) for field in INSIGHT_FIELDS}
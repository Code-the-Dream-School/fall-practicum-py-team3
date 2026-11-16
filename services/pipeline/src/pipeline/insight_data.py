from pipeline.extract.extract import CITIES


##Retrieve gold data for LLM insights.

PAGE_SIZE = 1000 

# Fields sent to the LLM prompt.
INSIGHT_FIELDS = ("city", "timestamp", "category", "aqi_24h_avg")


def _apply_filters(query, city, start, end):
    if city:
        query = query.eq("city", city)
    if start:
        query = query.gte("timestamp", start)
    if end:
        query = query.lte("timestamp", end)
    return query.order("city").order("timestamp")

def _fetch_all(client, table, city, start, end):
    # one city at a time, walking forward by timestamp. No OFFSET.
    names = [city] if city else list(CITIES)
    rows = []

    for name in names:
        cursor = None
        while True:
            query = _apply_filters(
                client.table(table).select("*"), name, start, end
            ).limit(PAGE_SIZE)
            # after the first page, pick up just past the last row we saw
            if cursor is not None:
                query = query.gt("timestamp", cursor)

            batch = query.execute().data or []
            if not batch:
                break

            rows.extend(batch)
            cursor = batch[-1]["timestamp"]

            if len(batch) < PAGE_SIZE:
                break

    return rows

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
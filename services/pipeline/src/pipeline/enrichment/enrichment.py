from pipeline.transform.transform import aqi_category
import json
import os
from datetime import datetime, timezone

from openai import OpenAI



def fallback_template(record):  
    category = aqi_category(round(record["aqi_24h_avg"]))
    return (
        f"{record['city']}'s air quality on {record['timestamp']} was {category}, "
        f"with a 24-hour average AQI of {record['aqi_24h_avg']}."
    )


BLOCKLIST = [
    "mask", "indoors", "outdoors", "asthma", "symptoms",
    "health", "exercise", "should", "avoid", "recommend",
]


def is_usable_insight(text):
    if not text or not isinstance(text, str):
        return False

    # 300 characters max
    if len(text) > 300:
        return False

    # reject words in the blocklist
    lowered = text.lower()
    for word in BLOCKLIST:
        if word in lowered:
            return False
        
    return True


#LLM stuff
PROMPT_VERSION = "insight-v3"
MODEL = "gpt-4o-mini"

WRITER_PROMPT = (
    "You write exactly one plain-language sentence about one U.S. city's air "
    "quality for one day, for a general reader. You are given the city, the "
    "date, the 24-hour average AQI, and its category. Use only these facts. "
    "Do not add numbers, causes, places or dates that are not in the input. "
    "Do not compare with other days. Do not give health advice, predict air "
    "quality, or tell people what to do. "
    'Reply only as JSON: {"insight_text": "..."}.'
)

FEW_SHOT_EXAMPLES = [
    (
        {"city": "Boston", "date": "2026-11-05", "aqi_24h_avg": 1.2, "category": "Good"},
        "Boston's air was in the Good range on November 5, with a 24-hour average AQI of 1.2.",
    ),
    (
        {"city": "Denver", "date": "2026-11-06", "aqi_24h_avg": 2.0, "category": "Fair"},
        "A Fair day for air quality in Denver on November 6, averaging an AQI of 2.0 over 24 hours.",
    ),
    (
        {"city": "Houston", "date": "2026-11-07", "aqi_24h_avg": 3.0, "category": "Moderate"},
        "Houston's 24-hour average AQI came in at 3.0 on November 7, putting the day in the Moderate category.",
    ),
    (
        {"city": "Phoenix", "date": "2026-11-08", "aqi_24h_avg": 3.6, "category": "Poor"},
        "Phoenix recorded Poor air quality on November 8, with a 24-hour average AQI of 3.6.",
    ),
    (
        {"city": "Fresno", "date": "2026-11-09", "aqi_24h_avg": 4.8, "category": "Very Poor"},
        "Fresno's air quality on November 9 was Very Poor, based on a 24-hour average AQI of 4.8.",
    ),
]


def call_llm(record):
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

    facts = {
        "city": record["city"],
        "date": str(record["timestamp"])[:10],
        "aqi_24h_avg": record["aqi_24h_avg"],
        "category": aqi_category(round(record["aqi_24h_avg"])),
    }

    messages = [{"role": "system", "content": WRITER_PROMPT}]

    for example_facts, example_text in FEW_SHOT_EXAMPLES:
        messages.append({"role": "user", "content": json.dumps(example_facts)})
        messages.append({"role": "assistant", "content": json.dumps({"insight_text": example_text})})

    messages.append({"role": "user", "content": json.dumps(facts)})

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        response_format={"type": "json_object"},
    )

    return json.loads(response.choices[0].message.content)



def enrich_record(record):
    if record.get("enriched_at"):
        return record

    result = dict(record)  # work on a copy
    try:
        data = call_llm(record)
        text = data.get("insight_text")

        if is_usable_insight(text):
            result["insight_source"] = "llm"
            result["model"] = MODEL
        else:                                      # use the template sentence instead    
            text = fallback_template(record)
            result["insight_source"] = "template"
            result["model"] = None

        result["insight_text"] = text
        result["prompt_version"] = PROMPT_VERSION
        result["enriched_at"] = datetime.now(timezone.utc).isoformat()
    except Exception as e:
        # LLM fails leave it un-enriched and save the reason
        result["enriched_at"] = None
        result["enrichment_error"] = str(e)

    return result



def enrich_records(records):
    # run enrich_record on every record in the list
    return [enrich_record(r) for r in records]



def run_enrichment(client, batch_size=500):
 
    rows = (
        client.table("daily_insight")
        .select("*")
        .is_("enriched_at", "null") #idempotency.
        .execute()
        .data
    )

    if not rows:
        print("Nothing to enrich.")
        return []
    results = enrich_records(rows)

    # write back in batches
    for start in range(0, len(results), batch_size):
        batch = results[start:start + batch_size]
        client.table("daily_insight").upsert(batch, on_conflict="city,timestamp").execute()

    failed = [r for r in results if r.get("enrichment_error")]
    print(f"Enriched {len(results) - len(failed)}, failed {len(failed)}.")
    return results
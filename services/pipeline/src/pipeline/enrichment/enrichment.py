from pipeline.load.load import supabase
from pipeline.transform.transform import aqi_category
from pipeline.run_tracking import start_run, finish_run, fail_run
import json
import os
from datetime import datetime, timezone

from openai import OpenAI

from dotenv import load_dotenv
load_dotenv()

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
PROMPT_VERSION = "insight-v1"
MODEL = "gpt-4o-mini"

# pagination for supabase
PAGE_SIZE = 1000

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

    result = dict(record) 
    try:
        data = call_llm(record)
        text = data.get("insight_text")

        if is_usable_insight(text):
            result["insight_source"] = "llm"
            result["model"] = MODEL
        else:           
            text = fallback_template(record)
            result["insight_source"] = "template"
            result["model"] = None

        result["insight_text"] = text
        result["prompt_version"] = PROMPT_VERSION
        result["enriched_at"] = datetime.now(timezone.utc).isoformat()
        result["enrichment_error"] = None    #clear any previous error if enrichment succeeds
    except Exception as e:
        result["enriched_at"] = None
        result["enrichment_error"] = str(e)

    return result



def enrich_records(records):
    # run enrich_record on every record in the list
    return [enrich_record(r) for r in records]


# unenriched
def get_unenriched_records(client, limit=None):
    rows = []
    offset = 0
    
    while True:
        page = (
            client.table("daily_insight")
            .select("*")
            .is_("enriched_at", "null")
            .order("city")
            .order("timestamp")
            .range(offset, offset + PAGE_SIZE - 1)
            .execute()
            .data or []
        )
        
        if limit is not None:
            remaining = limit - len(rows)
            page = page[:remaining]
            
        rows.extend(page)
        
        if limit is not None and len(rows) >= limit:
            break
        
        if len(page) < PAGE_SIZE:
            break
        
        offset += PAGE_SIZE
        
    return rows



def run_enrichment(client, batch_size=25, limit=None):
    run_id = start_run()
    rows_extracted = 0
    rows_transformed = 0
    rows_loaded = 0
    
    try:
        # read only rows that haven't been enriched yet (this is what makes reruns safe)
        # query = (
        #     client.table("daily_insight")
        #     .select("*")
        #     .is_("enriched_at", "null")
        # )
        # if limit:
        #     query = query.limit(limit)  # small test runs
        # rows = query.execute().data
        
        
        rows = get_unenriched_records(client, limit)
        
        # pipeline runs 
        rows_extracted = len(rows)

        if not rows:
            print("Nothing to enrich.")
            finish_run(
                run_id,
                rows_extracted=rows_extracted,
                rows_transformed=rows_transformed,
                rows_loaded=rows_loaded,
            )
            return []


        results = []
        for start in range(0, len(rows), batch_size):
            batch = rows[start:start + batch_size]
            batch_results = enrich_records(batch)
            results.extend(batch_results)
            
            rows_transformed += len(batch_results)
            
            # save enriched results to supabase
            client.table("daily_insight").upsert(
                batch_results,
                on_conflict="city,timestamp"
            ).execute()
            
            rows_loaded += len(batch_results)
            
            print(f"Enriched {len(results)} of {len(rows)}")
            
        failed = [r for r in results if r.get("enrichment_error")]
        print(f"Enriched {len(results) - len(failed)}, failed {len(failed)}.")
        finish_run(
            run_id,
            rows_extracted=rows_extracted,
            rows_transformed=rows_transformed,
            rows_loaded=rows_loaded,
        )
        return results
    
    except Exception as error:
        fail_run(
            run_id,
            error,
            rows_extracted=rows_extracted,
            rows_transformed=rows_transformed,
            rows_loaded=rows_loaded,
        )
        raise

if __name__ == "__main__":
    run_enrichment(supabase, batch_size=25, limit=None)
    
    
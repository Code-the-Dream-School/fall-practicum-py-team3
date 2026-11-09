from pipeline.transform.transform import aqi_category
import json
import os

from openai import OpenAI



def make_template_insight(record): 
    """build fallback sentence if the model fails to produce one"""
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

    # reject anything that sounds like health advice
    lowered = text.lower()
    for word in BLOCKLIST:
        if word in lowered:
            return False

    return True


#LLM stuff
PROMPT_VERSION = "insight-v2"
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


def call_llm(record):
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

    facts = {
        "city": record["city"],
        "date": str(record["timestamp"])[:10],
        "aqi_24h_avg": record["aqi_24h_avg"],
        "category": aqi_category(round(record["aqi_24h_avg"])),
    }

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": WRITER_PROMPT},
            {"role": "user", "content": json.dumps(facts)},
        ],
        response_format={"type": "json_object"},
    )

    return json.loads(response.choices[0].message.content)

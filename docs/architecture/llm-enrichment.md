# LLM Enrichment contract

## Unit of work: One Insight per city per day

# Which days get enriched, which are skipped

A Tracked City day is enriched only when all are true:

| Rule                                                 | Otherwise                 |
| ---------------------------------------------------- | ------------------------- |
| The day has ended (UTC)                              | skipped, `incomplete_day` |
| Gold rows cover at least 75% of its hours (18 of 24) | skipped, `low_coverage`   |
| It has no row yet with status `enriched`             | not sent (already done)   |

Why 75%: gold never fills or estimates missing hours, so a day with thin data would describe a few hours as a whole day.

## Facts Python computes (model input)

| Fact                                | Why the writer needs it                                      |
| ----------------------------------- | ------------------------------------------------------------ |
| 24-hour average AQI (`aqi_24h_avg`) | The day's level, smoothed so one bad hour does not decide it |
| AQI category of that average        | The label (Good, Fair, Moderate, Poor, Very Poor)            |

The category comes from `aqi_category()` applied to `aqi_24h_avg`, not to a single hourly score.

# Fields added

One row per (Tracked City, date). 1 enriched row = 1 day of hourly data.

### Insight table

| Field            | Type           | Allowed values                                                                                                |
| ---------------- | -------------- | ------------------------------------------------------------------------------------------------------------- |
| `insight_text`   | text, nullable | 1 English sentence, non-empty, ≤ 300 characters, passes the health-advice blocklist; `null` unless `enriched` |
| `insight_source` | text, nullable | `llm` (written by the model) or `template` (fallback); `null` unless `enriched`                               |

### Run metadata

| Field           | Type           | Allowed values                   |
| --------------- | -------------- | -------------------------------- |
| `status`        | text           | `enriched`, `skipped`, `failed`  |
| `skip_reason`   | text, nullable | `incomplete_day`, `low_coverage` |
| `error_message` | text, nullable | set only when `failed`           |

Primary key is `(city, date)`. Table name and DDL are settled in the coding ticket (the architecture model currently calls it `insights`).

## Prompts and where they live

Plain-text files in the repo, next to the enrichment code (`services/pipeline/src/pipeline/enrich/prompts/`), reviewed in PRs like code. Not in the database or environment variables. One version string (`insight-v2`) covers the writer prompt, the blocklist and the template; bump it on any wording change.

### Writer prompt (`insight-v2`)

> You write exactly one plain-language sentence about one U.S. city's air quality for one day, for a general reader. You are given the city, the date, the 24-hour average AQI, and its category. Use only these facts. Do not add numbers, causes, places or dates that are not in the input. Do not compare with other days. Do not give health advice, predict air quality, or tell people what to do. Reply only as JSON: {"insight_text": "..."}.

### Health-advice blocklist

Rejects text containing terms such as: mask, indoors, outdoors, asthma, symptoms, health, exercise, should, avoid, recommend. Health guidance belongs to Health Tips only.

# Template fallback

`{City}'s air quality on {Date} was {category}, with a 24-hour average AQI of {x}.`

Example: "Denver's air quality on 2024-03-14 was Moderate, with a 24-hour average AQI of 3.0."

## When the model returns something unusable

| What happens                                      | Result                                                                           |
| ------------------------------------------------- | -------------------------------------------------------------------------------- |
| Network error, 429 or 5xx                         | Retry up to 3 times with backoff, then `failed` with the error; retried next run |
| 400 or refusal                                    | Template writes the Insight; `insight_source = template`; day is `enriched`      |
| Empty, malformed JSON, too long, or blocklist hit | Template writes the Insight; `insight_source = template`; day is `enriched`      |
| Any failure                                       | Never stops the batch. The Pipeline Run counts enriched, skipped and failed days |

Transient errors leave the day `failed` rather than storing template text, so an OpenAI outage does not permanently replace Insights with the fallback.

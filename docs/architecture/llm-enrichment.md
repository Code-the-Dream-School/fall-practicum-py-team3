# LLM Enrichment contract

## Unit of work: One Insight per city for the month

# Which months get enriched, which are skipped

A Tracked City month is enriched only when all are true:

| Rule                                      | Otherwise                   |
| ----------------------------------------- | --------------------------- |
| The month has ended (UTC)                 | skipped, `incomplete_month` |
| Gold rows cover at least 75% of its hours | skipped, `low_coverage`     |
| It has no row yet with status `enriched`  | not sent (already done)     |

Why 75%: gold never fills or estimates missing hours, so a month with thin data would describe a few days as a whole month.

## Facts Python computes (model input)

| Fact                                     | Why the writer needs it                                                               |     |
| ---------------------------------------- | ------------------------------------------------------------------------------------- | --- |
| Hours covered, coverage %                | Lets the writer avoid overclaiming on a month with gaps; audit trail for the 75% rule |
| Mean of each of the 8 pollutants (µg/m³) | What the air was made of                                                              |
| Worst AQI Level in the month             | Gives the month's peak, which a mean hides                                            |
| Share of hours at each AQI Level         | Says how often the air was bad, not just how bad it got once                          |     |

# Fields added

One row per (Tracked City, month). 1 enriched row = 30 days of hourly data

### Insight table

| Field            | Type           | Allowed values                                                                                                   |
| ---------------- | -------------- | ---------------------------------------------------------------------------------------------------------------- |
| `insight_text`   | text, nullable | 1–2 English sentences, non-empty, ≤ 300 characters, passes the health-advice blocklist; `null` unless `enriched` |
| `insight_source` | text, nullable | `llm` (written by the model) or `template` (fallback); `null` unless `enriched`                                  |

### Run metadata

| Field         | Type           | Allowed values                     |
| ------------- | -------------- | ---------------------------------- |
| `status`      | text           | `enriched`, `skipped`, `failed`    |
| `skip_reason` | text, nullable | `incomplete_month`, `low_coverage` |

Table name and DDL are settled in the coding ticket (the architecture model currently calls it `insights`).

## Prompts and where they live

Plain-text files in the repo, next to the enrichment code (`services/pipeline/src/pipeline/enrich/prompts/`), reviewed in PRs like code. Not in the database or environment variables. One version string (`insight-v1`) covers the writer prompt, the blocklist and the template; bump it on any wording change.

### Writer prompt (`insight-v1`)

> You write one or two plain-language sentences about one U.S. city’s air quality for one month, for a general reader. Use only the facts given. Do not add numbers, causes, places or dates that are not in the input. Do not compare with other months or years. Do not give health advice, predict air quality, or tell people what to do. Reply as JSON: {"insight_text": "..."}.

### Health-advice blocklist

Rejects text containing terms such as: mask, indoors, outdoors, asthma, symptoms, health, exercise, should, avoid, recommend. Health guidance belongs to Health Tips only.

# Template fallback

`{City}'s air in {Month YYYY} peaked at {worst AQI label}, with {x}% of hours Fair or worse and a mean PM2.5 of {y} µg/m³.`

Example: "Denver's air in March 2024 peaked at Moderate, with 38% of hours Fair or worse and a mean PM2.5 of 9.4 µg/m³."

## When the model returns something unusable

| What happens                                      | Result                                                                             |
| ------------------------------------------------- | ---------------------------------------------------------------------------------- |
| Network error, 429 or 5xx                         | Retry up to 3 times with backoff, then `failed` with the error; retried next run   |
| 400 or refusal                                    | Template writes the Insight; `insight_source = template`; month is `enriched`      |
| Empty, malformed JSON, too long, or blocklist hit | Template writes the Insight; `insight_source = template`; month is `enriched`      |
| Any failure                                       | Never stops the batch. The Pipeline Run counts enriched, skipped and failed months |

Transient errors leave the month `failed` rather than storing template text, so an OpenAI outage does not permanently replace Insights with the fallback.

# LLM Enrichment contract

What the LLM adds to our data, decided before writing the code (sprint 3, deliverable 1). Terms follow [`CONTEXT.md`](../../CONTEXT.md). The model choice is in [ADR 0001](../adr/0001-use-openai-for-llm-enrichment.md). Status: **proposed**, pending team review.

Gold is hourly in the current code, so [team-decisions.md](../../team-documentation/team-decisions.md) (Granularity, Transform, Load) was updated to match it as part of this proposal.

## In one paragraph

For each completed calendar month of each Tracked City, Python computes the facts from the hourly gold table. `gpt-4o-mini`, called directly through the [OpenAI API](https://platform.openai.com/docs/api-reference/chat), turns the facts into a one- or two-sentence Insight. If the written text is unusable, a fixed template writes the Insight instead. Health Tips are not part of this stage and stay rule-based. Typed judgments (pollution profile, how unusual, getting worse) are out of scope.

## Unit of work: one Tracked City month

Gold (`gold_air_quality`) is hourly. Enriching hourly or daily rows would mean ~1.7M or ~70k calls with little to say each. One Tracked City month gives ~2,400 records for the full history and a natural size for a plain-language summary.

## Which months get enriched, which are skipped

A Tracked City month is enriched only when all are true:

| Rule | Otherwise |
|---|---|
| The month has ended (UTC) | skipped, `incomplete_month` |
| Gold rows cover at least 75% of its hours | skipped, `low_coverage` |
| It has no row yet with status `enriched` | not sent (already done) |

Why 75%: gold never fills or estimates missing hours, so a month with thin data would describe a few days as a whole month. This also handles the partial first month (November 2020).

Skipped months are stored with their reason, so "missing" and "not eligible" are distinguishable. `failed` months are retried on the next Pipeline Run.

**Re-enrichment:** one result per (city, month). A new prompt version or model does not reprocess old months automatically; a manual `--re-enrich` option does. Each row records its model and prompt version, so stale rows are easy to find.

## Facts Python computes (model input)

All numbers are computed in Python, never by the model: LLMs are weak at arithmetic and date comparison, and keeping numbers out of the model means every number on the dashboard can be traced to gold. The facts are stored with the result.

| Fact | Why the writer needs it |
|---|---|
| Hours covered, coverage % | Lets the writer avoid overclaiming on a month with gaps; audit trail for the 75% rule |
| Mean of each of the 8 pollutants (µg/m³) | What the air was made of |
| Worst AQI Level in the month | Gives the month's peak, which a mean hides |
| Share of hours at each AQI Level | Says how often the air was bad, not just how bad it got once |
| Change in mean PM2.5, O3, NO2 vs the same month a year earlier | The only comparison the writer may state. Same month last year cancels seasonal swings (ozone peaks in summer, PM in winter). `null` in the first 12 months |

## Fields added

One row per (Tracked City, month).

### Insight

| Field | Type | Allowed values |
|---|---|---|
| `insight_text` | text, nullable | 1–2 English sentences, non-empty, ≤ 300 characters, passes the health-advice blocklist; `null` unless `enriched` |
| `insight_source` | text, nullable | `llm` (written by the model) or `template` (fallback); `null` unless `enriched` |

### Run metadata

| Field | Type | Allowed values |
|---|---|---|
| `status` | text | `enriched`, `skipped`, `failed` |
| `skip_reason` | text, nullable | `incomplete_month`, `low_coverage` |
| `error` | text, nullable | last error message when `failed` |
| `attempts` | int | ≥ 1 |
| `model` | text, nullable | model ID used for the call, e.g. `gpt-4o-mini`; `null` when skipped |
| `prompt_version` | text | e.g. `insight-v1` |
| `facts` | JSON | exactly what the model was shown |
| `pipeline_run_id` | FK | the Pipeline Run that produced the row |
| `enriched_at` | timestamp (UTC) | |

Table name and DDL are settled in the coding ticket (the architecture model currently calls it `insights`).

## Prompts and where they live

Plain-text files in the repo, next to the enrichment code (`services/pipeline/src/pipeline/enrich/prompts/`), reviewed in PRs like code. Not in the database or environment variables. One version string (`insight-v1`) covers the writer prompt, the blocklist and the template; bump it on any wording change.

### Writer prompt (`insight-v1`)

> You write one or two plain-language sentences about one U.S. city's air quality for one month, for a general reader. Use only the facts given. Do not add numbers, causes, places or dates that are not in the input. Do not compare with earlier years unless a year-over-year change is given. Do not give health advice or tell people what to do. Reply as JSON: `{"insight_text": "..."}`.

The facts go in the user message as JSON. The call uses the [`openai` Python SDK](https://platform.openai.com/docs/api-reference/chat) (`client.chat.completions.create`) with `response_format: json_schema` and `strict: true`, as [documented for Structured Outputs](https://platform.openai.com/docs/guides/structured-outputs), which supports `gpt-4o-mini`. The schema fixes the shape (`insight_text`, string); length and the blocklist are checked in code. A safety refusal is reported by the API and treated as unusable output.

### Health-advice blocklist

Rejects text containing terms such as: mask, indoors, outdoors, asthma, symptoms, health, exercise, should, avoid, recommend. Health guidance belongs to Health Tips only.

### Template fallback

`{City}'s air in {Month YYYY} peaked at {worst AQI label}, with {x}% of hours Fair or worse and a mean PM2.5 of {y} µg/m³{trend clause}.`

The trend clause is ", up {z}% on a year earlier" or ", down {z}% on a year earlier" from the PM2.5 change, and empty when the change is `null`. Example: "Denver's air in March 2024 peaked at Moderate, with 38% of hours Fair or worse and a mean PM2.5 of 9.4 µg/m³, up 12% on a year earlier." Every number comes from the facts.

## When the model returns something unusable

| What happens | Result |
|---|---|
| Network error, 429 or 5xx | Retry up to 3 times with backoff, then `failed` with the error; retried next run |
| 400 or refusal | Template writes the Insight; `insight_source = template`; month is `enriched` |
| Empty, malformed JSON, too long, or blocklist hit | Template writes the Insight; `insight_source = template`; month is `enriched` |
| Any failure | Never stops the batch. The Pipeline Run counts enriched, skipped and failed months |

Transient errors leave the month `failed` rather than storing template text, so an OpenAI outage does not permanently replace Insights with the fallback.

## Testing

Tests mock the OpenAI client, so they run without an API key or cost. They cover each row of the table above, the skip rules, and re-running a month that is already `enriched` (no second call, no duplicate row).

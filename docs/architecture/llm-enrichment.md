# LLM Enrichment contract

What the LLM adds to our data, decided before writing the code (sprint 3, deliverable 1). Terms follow [`CONTEXT.md`](../../CONTEXT.md). The model choice is in [ADR 0001](../adr/0001-use-jev-for-insights.md). Status: **proposed**, pending team review.

Gold is hourly in the current code, so [team-decisions.md](../../team-documentation/team-decisions.md) (Granularity, Transform, Load) was updated to match it as part of this proposal.

## In one paragraph

For each completed calendar month of each Tracked City, Python computes the facts from the hourly gold table. [Jev](https://docs.aimlapi.com/api-references/decision-models/typesafe/jev) (`typesafe/jev-1.14`, via AI/ML API) makes three typed judgments about those facts. `gpt-4o-mini` turns facts and judgments into a one- or two-sentence Insight. If the written text is unusable, a fixed template writes the Insight instead. Health Tips are not part of this stage and stay rule-based.

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

All numbers are computed in Python, never by a model: LLMs are weak at arithmetic and date comparison, and keeping numbers out of the model means every number on the dashboard can be traced to gold. The facts are stored with the result.

| Fact | Why the models need it |
|---|---|
| Hours covered, coverage % | Lets the writer avoid overclaiming on a month with gaps; audit trail for the 75% rule |
| Mean of each of the 8 pollutants (µg/m³) | Basis for the pollution profile: the mix of pollutants is the only signal we have about what kind of air it was |
| Worst AQI Level in the month | Gives the month's peak, which a mean hides |
| Share of hours at each AQI Level | Says how often the air was bad, not just how bad it got once |
| Change in mean PM2.5, O3, NO2 vs the same month a year earlier | Basis for "getting worse". Same month last year cancels seasonal swings (ozone peaks in summer, PM in winter). `null` in the first 12 months |
| Z-score of each pollutant mean vs the city's own monthly history | Basis for unusualness. Compared to the city itself, not other cities, so a normally smoggy city is not "unusual" every month |

## Fields added

One row per (Tracked City, month).

### Judgments (Jev)

| Field | Type | Allowed values |
|---|---|---|
| `getting_worse_probability` | float, nullable | 0.0–1.0; Jev's `noul` answer (probability of "yes"); `null` when there is no year-earlier month |
| `getting_worse` | bool, nullable | `true` when `getting_worse_probability` ≥ 0.5, else `false`; `null` with it |
| `pollution_profile` | text | `traffic_combustion`, `smoke_particulate`, `dust`, `ozone_photochemical`, `industrial_sulfur`, `agricultural_ammonia`, `mixed`, `clean` |
| `pollution_profile_confidence` | float | 0.0–1.0; Jev's `confidence` for the choice |
| `unusualness` | float | 0.0–2.0; Jev's `score` on the legend `0` typical, `1` somewhat unusual, `2` very unusual (may be fractional) |
| `unusualness_label` | text | `typical`, `somewhat_unusual`, `very_unusual`: `unusualness` rounded to the nearest level |
| `unusualness_confidence` | float | 0.0–1.0; Jev's `confidence` for the score |

Answer shapes per the [Jev 1.14 reference](https://docs.aimlapi.com/api-references/decision-models/typesafe/jev-1.14.md): `noul` returns only the probability of "yes"; `choice` and `score` return a `confidence` (0–1) and per-option probabilities; `score` is the expected level on a legend we define. 0.5 and 0.7 (below) are starting values, to be tuned on a hand-labelled check set of ~30 months.

`pollution_profile` describes the mix of pollutants. It is not a cause: our data has no source information, so the dashboard must not present it as one.

### Insight (writer)

| Field | Type | Allowed values |
|---|---|---|
| `insight_text` | text | 1–2 English sentences, non-empty, ≤ 300 characters, passes the health-advice blocklist |
| `insight_source` | text | `llm` (written by `gpt-4o-mini`) or `template` (fallback) |

### Run metadata

| Field | Type | Allowed values |
|---|---|---|
| `status` | text | `enriched`, `skipped`, `failed` |
| `skip_reason` | text, nullable | `incomplete_month`, `low_coverage` |
| `error` | text, nullable | last error message when `failed` |
| `attempts` | int | ≥ 1 |
| `judge_model` | text | pinned Jev ID, e.g. `typesafe/jev-1.14` |
| `writer_model` | text, nullable | `gpt-4o-mini`; `null` if the template wrote the Insight without a call |
| `prompt_version` | text | e.g. `insight-v1` |
| `facts` | JSON | exactly what the models were shown |
| `pipeline_run_id` | FK | the Pipeline Run that produced the row |
| `enriched_at` | timestamp (UTC) | |

Table name and DDL are settled in the coding ticket (the architecture model currently calls it `insights`).

## Prompts and where they live

Plain-text files in the repo, next to the enrichment code (`services/pipeline/src/pipeline/enrich/prompts/`), reviewed in PRs like code. Not in the database or environment variables. One version string (`insight-v1`) covers the Jev questions, the writer prompt, the blocklist and the template; bump it on any wording change.

### Jev questions (`insight-v1`)

Request shape per the [Jev 1.14 reference](https://docs.aimlapi.com/api-references/decision-models/typesafe/jev-1.14.md): `state` is the facts as text; each question has a `type`, `instructions` and `criteria`. Questions:

- **`getting_worse`** (`noul`): "Compared with the same month a year earlier, is this city's air quality getting worse?" Criteria: judge only from the year-over-year changes given; a rise in PM2.5, O3 or NO2 counts as worse. Not asked when there is no year-earlier month.
- **`pollution_profile`** (`choice`, labels above): "Which label best describes this month's pollutant mix?" Criteria: judge only from the pollutant means; pick `mixed` when no pollutant stands out, `clean` when all are low.
- **`unusualness`** (`score`, legend `{0: typical, 1: somewhat unusual, 2: very unusual}`): "How unusual is this month for this city?" Criteria: judge only from the z-scores; `0` is a normal month, `2` is far outside the city's usual range.

### Writer prompt (`insight-v1`)

> You write one or two plain-language sentences about one U.S. city's air quality for one month, for a general reader. Use only the facts and judgments given. Do not add numbers, causes, places or dates that are not in the input. Do not give health advice or tell people what to do. When `getting_worse_probability` is between 0.3 and 0.7, or a judgment's confidence is below 0.7, describe that judgment as uncertain. Reply as JSON: `{"insight_text": "..."}`.

Output is constrained with `response_format: json_schema` (`insight_text`, string, max 300 characters), as documented for [gpt-4o-mini on AI/ML API](https://docs.aimlapi.com/api-references/text-models-llm/openai/gpt-4o-mini.md).

### Health-advice blocklist

Rejects text containing terms such as: mask, indoors, outdoors, asthma, symptoms, health, exercise, should, avoid, recommend. Health guidance belongs to Health Tips only.

### Template fallback

`{City}'s air in {Month YYYY} was {typical for the city | somewhat unusual for the city | very unusual for the city}, with {profile phrase}{trend clause}.`

The trend clause is "and looked worse than a year earlier" (probability ≥ 0.7), "and may have been worse than a year earlier" (0.5–0.7), "and looked no worse than a year earlier" (< 0.5), or empty when `getting_worse` is `null`. Example: "Denver's air in March 2024 was typical for the city, with an ozone-heavy pollutant mix, and looked worse than a year earlier."

## When the model returns something unusable

| What happens | Result |
|---|---|
| Jev: network error, 429 or 5xx | Retry up to 3 times with backoff, then `failed` with the error; retried next run |
| Jev: 400 or refusal | No retry this run; `failed` |
| Jev: missing answer, label not in the list, value outside its range above | Whole month `failed`; no partial judgments saved |
| Writer: error, empty, malformed JSON, too long, or blocklist hit | Template writes the Insight; `insight_source = template`; month is still `enriched` |
| Any failure | Never stops the batch. The Pipeline Run counts enriched, skipped and failed months |

## Testing

Tests mock both Jev and the writer, so they run without an API key or cost. They cover each row of the table above, the skip rules, and re-running a month that is already `enriched` (no second call, no duplicate row).

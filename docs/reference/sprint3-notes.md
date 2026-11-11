# Sprint 3 Reference: Backfilling vs. Incremental Loading

## Overview

A data pipeline loads data in one of two ways: **backfilling** or **incremental loading**. Backfilling loads a large amount of data at once. Incremental loading loads one small piece at a time. A well-built pipeline does both.

**Analogy:** Consider a magazine.
- **Backfilling** buys the whole archive of past issues at once.
- **Incremental loading** receives each new issue every week.

You want both: the archive for the past, the weekly delivery for the present.

## Incremental Loading

Incremental loading adds data in small chunks, repeatedly, as new data arrives.

**Example:** Every hour, you call a weather API and load that hour's data.

**Why it is needed:** Data that does not yet exist cannot be loaded. Next year's data cannot be loaded today, so you load it as it arrives. Without new data, your pipeline is current only as of today. Incremental loading supplies tomorrow's data, then the next day's, then the next.

**Choosing a frequency:** Your project's purpose determines how often you load.

- A forecasting product that updates hourly might fetch every 30 minutes.
- A real-time product might fetch every 30 seconds.
- Other projects might load every minute, hour, or week.

Whatever the interval, the work is incremental.

## Backfilling

Backfilling loads historical data that already exists at the source, usually in a single job.

**Example:** Your project needs a year of weather history. Do not fetch each day separately. Request the whole year and load it at once. This is more efficient, provided your functions support it.

**Changing requirements:** Months later, you need five years of data instead. Load the five years as a backfill. When your project's needs change, bulk load the history you need.

## Side-by-Side Comparison

| | Incremental Loading | Backfilling |
|---|---|---|
| **Data loaded** | New data as it arrives | Past data that already exists |
| **Size per run** | Small chunk | Large batch |
| **Frequency** | Repeatedly, on a schedule | Usually once, as needed |
| **Purpose** | Keep data current | Populate or repair history |

The chief difference: whether the data already exists.

## Why a Pipeline Should Support Both

**Incremental loading** keeps your data fresh.

**Backfilling** serves two purposes:

1. **Flexibility.** When requirements change and you need more history, you can load it in bulk.
2. **Error correction.** Backfilling repairs data you have already loaded. For example:
   - A bug in your incremental loading function requires you to reprocess old data.
   - The source publishes a corrected dataset, and you must replace what you loaded earlier.

## How to Build a Pipeline That Does Both

Write one loading function that accepts a **start time** and an **end time**. The two run types then differ only in the time range.

```python
def load_weather(start_time, end_time):
    """Load data where start_time <= observed_at < end_time."""
    data = fetch_weather_api(start_time, end_time)
    save_to_database(data)   # must be idempotent (Sprint 2)

# Incremental: runs on a schedule, e.g. every hour.
# Use clean hour boundaries so consecutive runs line up exactly.
load_weather(start_time="2026-11-10 08:00", end_time="2026-11-10 09:00")
load_weather(start_time="2026-11-10 09:00", end_time="2026-11-10 10:00")

# Backfill: run once (or whenever you need history)
load_weather(start_time="2025-01-01", end_time="2026-01-01")   # all of 2025
```

This is pseudocode; the details will vary with your project.

### Define Your Time Ranges Carefully

Each range includes its start and excludes its end. One run therefore ends exactly where the next begins, leaving neither gap nor overlap. If you instead use "one hour ago to now," `now` differs on every run, and records near the edges may be missed or loaded twice.

## Backfilling Depends on Idempotency

Backfills and reruns overlap with data you have already loaded.

If your writes are idempotent (a unique constraint plus `ON CONFLICT`), an overlapping backfill is safe: existing raw rows are skipped, and gold rows are refreshed by upsert. If your writes are not idempotent, every overlap creates duplicates.

### What About Corrections?

When the source publishes corrected values, raw's "never edit" rule seems to conflict with `DO NOTHING`. You have two choices:

- Keep raw as "first received," and accept that corrections go uncaptured.
- Include the value in the unique key. A corrected value is then stored as a *new* raw row with a new `fetched_at`, and gold uses the latest row for each observation.

Make this decision **before** you run a corrective backfill.

## Hazards

- **Duplicates:** A backfill over dates already loaded can duplicate rows. Make your writes idempotent.
- **API limits:** Some APIs limit how much data one request may return. Your backfill may then need to loop over smaller date ranges.
- **Inconsistent boundaries:** Overlapping or gapped ranges between runs cause missing or double-counted data.
- **Unchecked loads:** After a backfill, compare the row count with your expectation. For example, 365 days should yield 365 rows per city.

## Common Mistakes

- Writing separate code for incremental loads and backfills, instead of one function with a time range.
- Using "now" as a floating boundary, which produces overlaps or gaps.
- Running a backfill without idempotent writes.
- Backfilling without a plan for values that have changed.

## Takeaway

Incremental loading keeps your pipeline current. Backfilling populates, extends, or repairs the past. Design your pipeline to do both, and make every write idempotent so that overlaps are safe.

## Key Terms

- **Pipeline:** A program that moves data from a source (such as an API) to a destination (such as a database).
- **API:** A service from which you request data, such as a weather service.
- **Historical data:** Data from the past that already exists.
- **Stale data:** Data that is out of date because nothing new has been added.
- **Load:** Fetch data from the source and save it to the destination.
- **Idempotent:** Safe to repeat. Running the operation many times leaves the same end state as running it once (Sprint 2).

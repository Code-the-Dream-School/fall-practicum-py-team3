# Sprint 2 Reference: Raw and Gold Data, and Idempotent Writes

**Sprint goal:** Learn why pipelines keep raw data apart from gold data, and why every write should be safe to repeat.

> **Note:** The SQL in this document uses **PostgreSQL** syntax. Other databases handle duplicates differently. MySQL, for example, uses `INSERT IGNORE` or `ON DUPLICATE KEY UPDATE`.

---

## The Big Picture

```
API  ->    RAW table  ->     GOLD table     ->  Your app / dashboard
        (as received)     (cleaned & useful)
```

Data flows left to right. Each step keeps its own copy, so you can always go back one step.

---

## Part 1: Raw and Gold Data

### What is raw data?

Raw data is your input, untouched. In our projects, the raw data is the content of the responses we fetch from an **API**. If you fetch weather data, the raw data is the **JSON** that comes back.

Keep three points in mind:

- Raw data need not be the literal JSON blob. You may design a raw table **schema** that mirrors the shape of the API response.
- What matters is that the **content** is preserved as received.
- At the raw stage, you have only *collected* data. You have not transformed it, combined it, or analyzed it.

### What is gold data?

Gold data is raw data, cleaned and formatted for use. It serves the project or product you are building. Depending on the project, it may include summaries, medians, means, labels, or other derived values.

**Examples:**

- **Historical trends:** the median over the last 7, 30, and 60 days.
- **Forecasting:** the average of the last 30 days, plus an adjustment for today's weather.

As a rule of thumb, **gold data is what your application cares about.**

### A concrete example

Suppose we fetch daily air quality (AQI) data for Burlington.

**Raw table** (exactly what the API gave us):

| id | city | aqi | observed_at | fetched_at |
|---|---|---|---|---|
| 1 | Burlington | 38 | 2026-11-04 | 2026-11-04 09:00 |
| 2 | Burlington | 45 | 2026-11-05 | 2026-11-05 09:00 |
| 3 | Burlington | 51 | 2026-11-06 | 2026-11-06 09:00 |
| 4 | Burlington | 40 | 2026-11-07 | 2026-11-07 09:00 |
| 5 | Burlington | 42 | 2026-11-08 | 2026-11-08 09:00 |
| 6 | Burlington | 67 | 2026-11-09 | 2026-11-09 09:00 |
| 7 | Burlington | 155 | 2026-11-10 | 2026-11-10 09:00 |

The two timestamps mean different things:

- `observed_at`: when the measurement *happened*. It comes from the source.
- `fetched_at`: when *we* collected it. We record it ourselves.

The `id` is a row number the database assigns. It identifies the *row*, not the *observation*. What counts as "the same observation" is a separate question, which a unique constraint answers in Part 2.

**Gold table** (what our app uses):

| city | date | aqi | label | median_7_day |
|---|---|---|---|---|
| Burlington | 2026-11-10 | 155 | unhealthy | 45 |

The 7-day median is the middle of the last seven readings (38, 40, 42, 45, 51, 67, 155), or 45. The label follows the US AQI scale, on which 151–200 is "unhealthy."

If a label looks wrong, compare the gold row with the raw rows. You will learn whether the API sent a bad number or our label logic has a bug.

> **Rules for raw data:** Never edit it. Never delete it. Record when you fetched it (`fetched_at`) and where it came from.

> **Note:** This pattern is often called the *medallion architecture*: **bronze** (raw), **silver** (cleaned), **gold** (ready for use). We use a simplified two-layer version.

### Why keep them separate?

Raw data is your **source of truth**, the one trusted record from which everything else derives. Once you have built gold data, do not discard the original observations. Three reasons follow.

#### 1. Debugging

Transformations are often complex and conditional, and mistakes come easily. Suppose you label air quality, with one threshold meaning "green" and another "yellow." If the labels look wrong, you must find the cause:

- Did you implement the threshold as intended?
- Was the input what you expected?

Without the raw data, you cannot answer these questions. For debugging, raw data is your most valuable asset.

#### 2. Auditing

Raw data lets you examine what you actually collected before you build on it.

*Example:* You are saving raw hotel reservations and want to add a feature that depends on reservation state. You do not yet know every possible value (booked but unpaid? not yet paid? something else?). Examine the distribution of values in the raw data, and you will find every state that occurs and can handle each one.

#### 3. New features without re-pulling data

Because raw data is preserved, you can add transformations later. You can build a `gold` table, then a `gold_v2` table, without re-fetching anything from the source.

### Key takeaway

Raw data records what happened. Gold data interprets it for a specific purpose. Keep both, and keep them separate.

---

## Part 2: Idempotent Writes

### What is idempotency?

**Idempotent means safe to repeat.**

More precisely, an operation is idempotent if performing it many times produces the same result as performing it once. You can make an API call, call a function, or run an operation twice, and your code will recognize the duplicate and ignore it.

> **Simple mental model:** Repeat an operation, and the end state is the same.

*Example:* You insert a row for a house whose address must be unique. The end state is one house with that address. If the insert runs again, exactly one such house remains, however many times it runs.

The same idea in code:

```python
balance = 100      # idempotent: run it 5 times, balance is still 100
balance += 100     # NOT idempotent: starting at 100, run it 5 times, balance is 600
```

The first line **sets** the state to a specific value. The second **changes** the state relative to its current value. Operations that set a known end state are safe to repeat. Operations that build on the current state need protection.

### Why does it matter?

Repeats happen, by design and by accident:

- A bug in the calling code invokes a function twice.
- A network error causes an API call or database write to be retried.
- A job crashes partway through and must be rerun.
- A scheduler occasionally runs a job twice (you will see this in Sprint 4).

You need a defense. The core idea: if the requested operation has already been done, do not do it again.

### Why it matters most for database writes

#### Data integrity (the main concern)

If data has been written, do not overwrite or duplicate it. Mistakes here can seriously harm users.

*Example:* A pipeline exports expenses to accounting software. The job dies halfway, and you rerun it. If the pipeline is not idempotent, someone may be double-charged in their books. Consequences like this make data integrity the chief reason for idempotency.

#### Cost and efficiency

Avoiding repeated work also matters:

- Writing a row twice wastes the work of writing it once.
- Running a function and writing to a database cost money. Returning "already written" costs far less than repeating the write.
- When you **backfill** (load historical data you did not collect earlier), the savings are large. Suppose you have written five years of data, and a bug fetches and writes those five years again. Your write logic should recognize that the data exists and skip it.

Both concerns are valid, but **data integrity is the primary one.**

### Idempotent writes in SQL

Here is the raw table we will use. It records both `observed_at` and `fetched_at`:

```sql
CREATE TABLE raw_weather (
    id          INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    city        TEXT NOT NULL,
    observed_at TIMESTAMP NOT NULL,
    temp_f      NUMERIC NOT NULL,
    fetched_at  TIMESTAMP NOT NULL DEFAULT now()
);
```

**Not idempotent.** Run twice, this creates two rows:

```sql
INSERT INTO raw_weather (city, observed_at, temp_f)
VALUES ('Burlington', '2026-11-10 09:00', 38);
```

**Idempotent.** First, define a `constraint` that tells the database what makes an observation unique:

```sql
ALTER TABLE raw_weather
ADD CONSTRAINT uq_city_time UNIQUE (city, observed_at);
```

The constraint is separate from `id`. The `id` identifies a row; the constraint defines a duplicate. Then ignore duplicates:

```sql
INSERT INTO raw_weather (city, observed_at, temp_f)
VALUES ('Burlington', '2026-11-10 09:00', 38)
ON CONFLICT (city, observed_at) DO NOTHING;
```

Run it once or a hundred times, and exactly one row remains.

#### Why a unique constraint, not a check first?

You might think: "I'll `SELECT` to see whether the row exists, then `INSERT` if it does not." But two runs can check at the same moment, both find nothing, and both insert. A **constraint**, a rule the database enforces, lets the database itself guarantee uniqueness. Nothing can bypass it. For the same reason, "checking for duplicates in Python" appears under Common Mistakes below.

#### DO NOTHING vs. upsert

| Approach | On a duplicate | Use when |
|---|---|---|
| `ON CONFLICT DO NOTHING` | Keeps the existing row; skips the new one | Raw data you never want to change |
| `ON CONFLICT DO UPDATE` (upsert) | Updates the existing row with the new values | Gold data you recompute and want refreshed |

Both are idempotent: repeating them leaves the same end state.

Here is an upsert for a gold table. It also needs a unique constraint, here on `(city, date)`:

```sql
INSERT INTO gold_daily (city, date, aqi, label)
VALUES ('Burlington', '2026-11-10', 155, 'unhealthy')
ON CONFLICT (city, date)
DO UPDATE SET aqi = EXCLUDED.aqi, label = EXCLUDED.label;
```

`EXCLUDED` refers to the row you tried to insert, so the statement reads: "set `aqi` to the new value." Rerunning it gives the same end state. If the inputs changed, gold is refreshed.

#### A trade-off with DO NOTHING: corrected values

`DO NOTHING` keeps the *first* value it sees. If the API later corrects a reading, the raw table silently keeps the old one. You have two options, and the right choice depends on the project:

- **Accept it.** Raw means "what we first received." This is simple, but corrections are lost.
- **Make the value part of the key.** For example, `UNIQUE (city, observed_at, temp_f)`. Identical repeats are still ignored, but a *changed* value is stored as a new raw row with a new `fetched_at`. Gold then picks the most recently fetched row for each observation.

The second option honors "never edit raw" and still admits corrections.

### What about operations that cannot be repeated safely?

Some actions, such as sending an email or charging a credit card, have real-world side effects that cannot be undone. Handle these with an **idempotency key**: a unique ID sent with the request, so the receiving system can recognize a repeat and ignore it. Payment APIs such as Stripe work this way.

---

## Common Mistakes

- Overwriting raw data after cleaning it ("I'll just fix it in place").
- Inserting rows without a unique constraint, so a rerun creates duplicates.
- Checking for duplicates in Python instead of letting the database enforce uniqueness.
- Building a pipeline that works only the first time it runs.
- Confusing the row `id` with what makes an observation unique.
- Never checking what landed in the table after a load (see below).

---

## Check Your Load

A pipeline that runs without errors can still load the wrong data. After a load, make three quick checks:

- **Row count:** Did the number of rows change by the expected amount?
- **Duplicates:** Does a `GROUP BY city, observed_at HAVING COUNT(*) > 1` query return nothing?
- **Missing values:** Are any required columns empty?

```sql
SELECT city, observed_at, COUNT(*)
FROM raw_weather
GROUP BY city, observed_at
HAVING COUNT(*) > 1;   -- should return zero rows
```

---

## Quick Reference

| Concept | Core idea | Why it matters |
|---|---|---|
| **Raw data** | Untouched data as collected from the source | Source of truth; enables debugging, auditing, and future features |
| **Gold data** | Cleaned, transformed data that serves your application | What your product or analysis uses |
| **Idempotency** | Repeating an operation yields the same end state | Protects data integrity; avoids wasted work |
| **Unique constraint** | A database rule defining a duplicate | Makes idempotent writes enforceable |

## Pipeline Checklist

1. Do I store the raw data exactly as collected, before any transformation?
2. If my gold data looks wrong, can I trace it to the raw data and find the cause?
3. If I add a gold table later, do I have what I need without re-pulling from the source?
4. If this write runs twice, is the end state the same?
5. If this job fails halfway and is rerun, what happens?
6. After the load, do the row counts and duplicate checks look right?

---

## Glossary

| Term | Plain-English meaning |
|---|---|
| **API** | A way for programs to request data from another service |
| **Backfill** | Loading historical data you did not collect earlier |
| **Constraint** | A rule the database enforces, such as "this column must be unique" |
| **fetched_at** | When your pipeline

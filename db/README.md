# Database

PostgreSQL on Supabase. Schema files live in this folder, numbered, and are
applied in numeric order.

## How to run

1. Supabase project → SQL Editor → New query.
2. Paste the contents of `001_pipeline_runs.sql` and click Run.
3. Run it a second time. It should succeed with no changes — the file is
   written to be safe to repeat.

Starting from an empty database means running each file from 001 upward.
No tables need to be created by hand.

Expect "Success. No rows returned." — `CREATE` statements don't return rows.

## Changing the schema

`CREATE TABLE IF NOT EXISTS` skips a table that already exists, so editing a
file and re-running it will not change the table. While there is no data worth
keeping, drop and recreate:

```sql
DROP TABLE IF EXISTS pipeline_runs;
```

Once the table holds real data, changes go in a new numbered file using
`ALTER TABLE` instead.

## 001_pipeline_runs.sql — `pipeline_runs`

One row per pipeline run, recording when the run started and ended, whether it
succeeded, and how many rows moved through each stage. Timestamps are the
processing time of the run itself, not the date range of the data it pulled.

**Primary key:** `pipeline_run_id`. A generated identity — Postgres assigns
1, 2, 3… automatically. Never null, never duplicated.

**Foreign keys:** none. This table does not reference any other table.

**Uniqueness:** `run_id` is `UNIQUE`. One pipeline execution produces exactly
one row, so a run can never be recorded twice.

**Required columns:** `pipeline_run_id`, `run_id`, `status`, `started_at`.
The rest are nullable because their values are not known until the run
finishes. A NULL count means that stage never completed, which is different
from a count of zero.

| Column             | Type        | Required                    | Meaning                                      |
| ------------------ | ----------- | --------------------------- | -------------------------------------------- |
| `pipeline_run_id`  | BIGINT      | Yes (auto-generated)        | Primary key                                  |
| `run_id`           | TEXT        | Yes                         | Identifier for the run, e.g. a UTC timestamp |
| `status`           | TEXT        | Yes (defaults to `running`) | `running`, `succeeded`, or `failed`          |
| `started_at`       | TIMESTAMPTZ | Yes (defaults to `now()`)   | When the run began                           |
| `finished_at`      | TIMESTAMPTZ | No                          | When it ended; NULL while still running      |
| `rows_extracted`   | INTEGER     | No                          | Rows pulled from the source                  |
| `rows_loaded`      | INTEGER     | No                          | Rows written to raw                          |
| `rows_transformed` | INTEGER     | No                          | Rows written to gold                         |
| `error_message`    | TEXT        | No                          | Why the run failed                           |

`status` is constrained to those three values by
`pipeline_runs_status_check`, so a typo cannot get into the table.

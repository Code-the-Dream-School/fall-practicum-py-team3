## 001_pipeline_runs.sql — `pipeline_runs`

One row per pipeline run, recording when the run started and ended, whether it
succeeded, and how many rows moved through each stage. Timestamps are the
processing time of the run itself, not the date range of the data it pulled.

**Primary key:** `run_id`. A BIGINT generated identity — Postgres assigns
1, 2, 3… automatically. Never null, never duplicated.

**Foreign keys:** none. This table does not reference any other table.

**Uniqueness:** `run_id`, enforced by the primary key. One pipeline execution
produces exactly one row.

**Required columns:** `run_id`, `created_at`, and `status`. Everything else is
nullable, and the nulls carry meaning — a NULL count means that stage never
ran, which is different from a count of 0.

| Column | Type | Required | Meaning |
|---|---|---|---|
| `run_id` | BIGINT | Yes (auto-generated) | Primary key |
| `created_at` | TIMESTAMPTZ | Yes (defaults to `now()`) | When the record was created |
| `started_at` | TIMESTAMPTZ | No | When the run actually began; NULL while pending |
| `ended_at` | TIMESTAMPTZ | No | When it ended; NULL while still running |
| `status` | TEXT | Yes (defaults to `pending`) | `pending`, `running`, `success`, or `failed` |
| `rows_extracted` | INTEGER | No | Rows pulled from the source |
| `rows_transformed` | INTEGER | No | Rows written to gold |
| `rows_loaded` | INTEGER | No | Rows written to raw |
| `error_message` | TEXT | No | Why the run failed |

`status` is constrained to those four values by `pipeline_runs_status_check`,
so a typo cannot get into the table.
